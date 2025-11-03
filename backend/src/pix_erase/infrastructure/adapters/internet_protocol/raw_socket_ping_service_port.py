import asyncio
import os
import socket
import struct
import select
import time
import platform
import threading
import zlib
from typing import Final, override
import logging

from pix_erase.domain.internet_protocol.errors.internet_protocol import (
    PingTimeoutError,
    PingDestinationUnreachableError,
    PingTimeExceededError,
    PingPermissionError,
    PingNetworkError,
)
from pix_erase.domain.internet_protocol.ports.ping_service_port import PingServicePort
from pix_erase.domain.internet_protocol.values.ip_address import IPAddress, IPv4Address, IPv6Address
from pix_erase.domain.internet_protocol.values.ping_result import PingResult

logger = logging.getLogger(__name__)

# ICMP constants
ICMP_HEADER_FORMAT: Final[str] = "!BBHHH"  # Type, Code, Checksum, ID, Sequence
ICMP_TIME_FORMAT: Final[str] = "!d"  # Double for timestamp
ICMP_DEFAULT_CODE: Final[int] = 0
ICMP_ECHO_REQUEST: Final[int] = 8
ICMP_ECHO_REPLY: Final[int] = 0
ICMP_TIME_EXCEEDED: Final[int] = 11
ICMP_DESTINATION_UNREACHABLE: Final[int] = 3

# IPv6 constants
ICMPV6_ECHO_REQUEST: Final[int] = 128
ICMPV6_ECHO_REPLY: Final[int] = 129
ICMPV6_TIME_EXCEEDED: Final[int] = 3
ICMPV6_DESTINATION_UNREACHABLE: Final[int] = 1

# IPv6 pseudo header format
ICMPV6_PSEUDO_HEADER_FORMAT: Final[str] = "!16s16sIBBBB"

# IP header formats
IPV4_HEADER_FORMAT: Final[str] = "!BBHHHBBHII"  # IPv4 header
IPV6_HEADER_FORMAT: Final[str] = "!IHBB16s16s"  # IPv6 header


class RawSocketPingServicePort(PingServicePort):
    """
    Raw socket implementation of ping service.
    
    This implementation uses raw sockets to send ICMP packets directly,
    providing low-level control over the ping process.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()

    @override
    async def ping(
            self,
            destination: IPAddress,
            timeout: float = 4.0,
            packet_size: int = 56,
            ttl: int | None = None,
    ) -> PingResult:
        """
        Ping a destination IP address using raw sockets.
        
        Args:
            destination: The IP address to ping
            timeout: Timeout in seconds
            packet_size: Size of the ping packet in bytes
            ttl: Time to live for the packet
            
        Returns:
            PingResult containing the ping result information
        """
        try:
            if isinstance(destination, IPv4Address):
                return await self._ping_ipv4(destination, timeout, packet_size, ttl)
            elif isinstance(destination, IPv6Address):
                return await self._ping_ipv6(destination, timeout, packet_size, ttl)
            else:
                raise PingNetworkError(f"Unsupported IP address type: {type(destination)}")
        except Exception as e:
            if isinstance(e, (
                    PingTimeoutError,
                    PingDestinationUnreachableError,
                    PingTimeExceededError,
                    PingPermissionError,
                    PingNetworkError,
            )):
                raise
            raise PingNetworkError(f"Unexpected error during ping: {e}") from e

    @override
    async def ping_multiple(
            self,
            destinations: list[IPAddress],
            timeout: float = 4.0,
            packet_size: int = 56,
            ttl: int | None = None,
    ) -> list[PingResult]:
        """
        Ping multiple destination IP addresses concurrently.
        
        Args:
            destinations: List of IP addresses to ping
            timeout: Timeout in seconds for each ping
            packet_size: Size of the ping packet in bytes
            ttl: Time to live for the packet
            
        Returns:
            List of PingResult objects in the same order as destinations
        """
        tasks = [
            self.ping(dest, timeout, packet_size, ttl)
            for dest in destinations
        ]
        return await asyncio.gather(*tasks)

    async def _ping_ipv4(
            self,
            destination: IPv4Address,
            timeout: float,
            packet_size: int,
            ttl: int | None,
    ) -> PingResult:
        """Ping an IPv4 address."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except PermissionError as e:
            if e.errno == 1:  # Operation not permitted
                logger.warning("Raw socket requires elevated permissions, trying SOCK_DGRAM")
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
            else:
                raise PingPermissionError("Failed to create socket") from e

        try:
            # Set TTL if provided
            if ttl:
                try:
                    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
                except OSError as e:
                    logger.warning(f"Failed to set TTL: {e}")

            # Generate unique ICMP ID
            icmp_id = self._generate_icmp_id()
            seq = 0

            # Send ping
            start_time = time.time()
            self._send_icmp_packet(sock, destination.value, icmp_id, seq, packet_size)

            # Receive response using select (like original library)
            response_time = await self._receive_icmp_response_select(
                sock, icmp_id, seq, timeout, start_time
            )

            return PingResult(
                response_time_ms=response_time * 1000,
                success=True,
                ttl=ttl,
                packet_size=packet_size,
            )

        except Exception as e:
            if isinstance(e, (
                    PingTimeoutError,
                    PingDestinationUnreachableError,
                    PingTimeExceededError,
            )):
                raise
            raise PingNetworkError(f"IPv4 ping failed: {e}") from e
        finally:
            sock.close()

    async def _ping_ipv6(
            self,
            destination: IPv6Address,
            timeout: float,
            packet_size: int,
            ttl: int | None,
    ) -> PingResult:
        """Ping an IPv6 address."""
        try:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_ICMPV6)
        except PermissionError as e:
            if e.errno == 1:  # Operation not permitted
                raise PingPermissionError("Raw socket requires elevated permissions") from e
            raise PingNetworkError(f"Failed to create socket: {e}") from e

        try:
            # Set TTL if provided
            if ttl:
                try:
                    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_UNICAST_HOPS, ttl)
                except OSError as e:
                    logger.warning(f"Failed to set TTL: {e}")

            # Generate unique ICMP ID
            icmp_id = self._generate_icmp_id()
            seq = 0

            # Send ping
            start_time = time.time()
            self._send_icmpv6_packet(sock, destination.value, icmp_id, seq, packet_size)

            # Receive response using select
            response_time = await self._receive_icmpv6_response_select(
                sock, icmp_id, seq, timeout, start_time
            )

            return PingResult(
                response_time_ms=response_time * 1000,
                success=True,
                ttl=ttl,
                packet_size=packet_size,
            )

        except Exception as e:
            if isinstance(e, (
                    PingTimeoutError,
                    PingDestinationUnreachableError,
                    PingTimeExceededError,
            )):
                raise
            raise PingNetworkError(f"IPv6 ping failed: {e}") from e
        finally:
            sock.close()

    @staticmethod
    def _generate_icmp_id() -> int:
        """Generate a unique ICMP ID."""
        thread_id = threading.get_native_id() if hasattr(threading, "get_native_id") else threading.current_thread().ident
        process_id = os.getpid()
        return zlib.crc32(f"{process_id}{thread_id}".encode()) & 0xffff

    def _send_icmp_packet(
            self,
            sock: socket.socket,
            destination: str,
            icmp_id: int,
            seq: int,
            packet_size: int,
    ) -> None:
        """Send an ICMP echo request packet."""
        # Create ICMP header
        icmp_header = struct.pack(
            ICMP_HEADER_FORMAT,
            ICMP_ECHO_REQUEST,
            ICMP_DEFAULT_CODE,
            0,  # Checksum (calculated later)
            icmp_id,
            seq,
        )

        # Create payload with timestamp
        timestamp = time.time()
        payload = struct.pack(ICMP_TIME_FORMAT, timestamp)
        padding_size = max(0, packet_size - len(payload))
        payload += b'Q' * padding_size

        # Calculate checksum
        checksum = self._calculate_checksum(icmp_header + payload)
        icmp_header = struct.pack(
            ICMP_HEADER_FORMAT,
            ICMP_ECHO_REQUEST,
            ICMP_DEFAULT_CODE,
            socket.htons(checksum),
            icmp_id,
            seq,
        )

        # Send packet
        packet = icmp_header + payload
        sock.sendto(packet, (destination, 0))

    def _send_icmpv6_packet(
            self,
            sock: socket.socket,
            destination: str,
            icmp_id: int,
            seq: int,
            packet_size: int,
    ) -> None:
        """Send an ICMPv6 echo request packet."""
        # Create ICMPv6 header
        icmp_header = struct.pack(
            ICMP_HEADER_FORMAT,
            ICMPV6_ECHO_REQUEST,
            ICMP_DEFAULT_CODE,
            0,  # Checksum (calculated later)
            icmp_id,
            seq,
        )

        # Create payload with timestamp
        timestamp = time.time()
        payload = struct.pack(ICMP_TIME_FORMAT, timestamp)
        padding_size = max(0, packet_size - len(payload))
        payload += b'Q' * padding_size

        # Get source address for pseudo header
        try:
            with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as dummy_sock:
                dummy_sock.connect((destination, 0))
                src_addr = dummy_sock.getsockname()[0]
        except Exception:
            src_addr = "::1"  # Fallback to loopback

        # Create pseudo header for checksum calculation
        pseudo_header = struct.pack(
            ICMPV6_PSEUDO_HEADER_FORMAT,
            socket.inet_pton(socket.AF_INET6, src_addr),
            socket.inet_pton(socket.AF_INET6, destination),
            len(icmp_header) + len(payload),
            0, 0, 0,  # Zeros
            ICMPV6_ECHO_REQUEST,
        )

        # Calculate checksum
        checksum = self._calculate_checksum(pseudo_header + icmp_header + payload)
        icmp_header = struct.pack(
            ICMP_HEADER_FORMAT,
            ICMPV6_ECHO_REQUEST,
            ICMP_DEFAULT_CODE,
            socket.htons(checksum),
            icmp_id,
            seq,
        )

        # Send packet
        packet = icmp_header + payload
        sock.sendto(packet, (destination, 0, 0, 0))

    @staticmethod
    def _calculate_checksum(data: bytes) -> int:
        """Calculate ICMP checksum using the same algorithm as ping3."""
        BITS = 16  # 16-bit long
        carry = 1 << BITS  # 0x10000
        result = sum(data[::2]) + (sum(data[1::2]) << (BITS // 2))  # Even bytes (odd indexes) shift 1 byte to the left.
        while result >= carry:  # Ones' complement sum.
            result = sum(divmod(result, carry))  # Each carry add to right most bit.
        return ~result & ((1 << BITS) - 1)  # Ensure 16-bit

    @staticmethod
    def _detect_ip_header(sock: socket.socket, recv_data: bytes) -> bool:
        """Detect if the received data has an IP header (like in original library)."""
        first_field = recv_data[0] >> 4  # The first 4 bits of the first byte is the version field of IP Header.
        return first_field == (4 if sock.family == socket.AF_INET else 6)

    @staticmethod
    async def _receive_icmp_response_select(
            sock: socket.socket,
            icmp_id: int,
            seq: int,
            timeout: float,
            start_time: float,
    ) -> float:
        """Receive ICMP response for IPv4 using select (like original library)."""
        timeout_time = start_time + timeout
        
        while True:
            timeout_left = timeout_time - time.time()
            timeout_left = max(0.0, timeout_left)  # Timeout must be non-negative
            
            # Use select to wait for data (like original library)
            ready, _, _ = select.select([sock], [], [], timeout_left)
            if not ready:  # Timeout
                raise PingTimeoutError(f"Ping timeout after {timeout} seconds")
            
            time_recv = time.time()
            recv_data, addr = sock.recvfrom(1500)
            
            # Detect if we have IP header (Windows behavior)
            has_ip_header = (os.name != "posix") or (platform.system() == "Darwin") or (sock.type == socket.SOCK_RAW)
            
            if has_ip_header:
                # Skip IP header (20 bytes for IPv4)
                icmp_start = 20
                icmp_header = recv_data[icmp_start:icmp_start + 8]
            else:
                # No IP header (Linux unprivileged)
                icmp_start = 0
                icmp_header = recv_data[icmp_start:icmp_start + 8]
            
            # Parse ICMP header
            type_code, code, checksum, recv_id, recv_seq = struct.unpack(
                ICMP_HEADER_FORMAT, icmp_header
            )
            
            # Check for error responses
            if type_code == ICMP_TIME_EXCEEDED:
                raise PingTimeExceededError("Time exceeded (TTL expired)")
            elif type_code == ICMP_DESTINATION_UNREACHABLE:
                raise PingDestinationUnreachableError("Destination unreachable")
            
            # Check if this is our echo reply
            if recv_id == icmp_id and recv_seq == seq and type_code == ICMP_ECHO_REPLY:
                # Extract timestamp from payload
                payload_start = icmp_start + 8
                timestamp = struct.unpack(ICMP_TIME_FORMAT, recv_data[payload_start:payload_start + 8])[0]
                return time_recv - float(timestamp)
            
            # Handle case where kernel rewrites ICMP ID (Linux unprivileged)
            if not has_ip_header and recv_id != icmp_id:
                # Try using port number as ICMP ID
                port_id = sock.getsockname()[1]
                if recv_id == port_id and recv_seq == seq and type_code == ICMP_ECHO_REPLY:
                    payload_start = icmp_start + 8
                    timestamp = struct.unpack(ICMP_TIME_FORMAT, recv_data[payload_start:payload_start + 8])[0]
                    return time_recv - float(timestamp)

    async def _receive_icmpv6_response_select(
            self,
            sock: socket.socket,
            icmp_id: int,
            seq: int,
            timeout: float,
            start_time: float,
    ) -> float:
        """Receive ICMPv6 response for IPv6 using select."""
        timeout_time = start_time + timeout
        
        while True:
            timeout_left = timeout_time - time.time()
            timeout_left = max(0.0, timeout_left)
            
            # Use select to wait for data
            ready, _, _ = select.select([sock], [], [], timeout_left)
            if not ready:  # Timeout
                raise PingTimeoutError(f"Ping timeout after {timeout} seconds")
            
            time_recv = time.time()
            recv_data, addr = sock.recvfrom(1500)
            
            # Detect if we have IP header
            has_ip_header = self._detect_ip_header(sock, recv_data)
            
            if has_ip_header:
                # Skip IPv6 header (40 bytes)
                icmp_start = 40
                icmp_header = recv_data[icmp_start:icmp_start + 8]
            else:
                # No IP header
                icmp_start = 0
                icmp_header = recv_data[icmp_start:icmp_start + 8]
            
            # Parse ICMP header
            type_code, code, checksum, recv_id, recv_seq = struct.unpack(
                ICMP_HEADER_FORMAT, icmp_header
            )
            
            # Check for error responses
            if type_code == ICMPV6_TIME_EXCEEDED:
                raise PingTimeExceededError("Time exceeded (TTL expired)")
            elif type_code == ICMPV6_DESTINATION_UNREACHABLE:
                raise PingDestinationUnreachableError("Destination unreachable")
            
            # Check if this is our echo reply
            if recv_id == icmp_id and recv_seq == seq and type_code == ICMPV6_ECHO_REPLY:
                # Extract timestamp from payload
                payload_start = icmp_start + 8
                timestamp = struct.unpack(ICMP_TIME_FORMAT, recv_data[payload_start:payload_start + 8])[0]
                return float(time_recv - timestamp)