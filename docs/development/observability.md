# Observability

The PixErase API integrates observability tools to monitor performance, logs, and traces, ensuring robust production monitoring.

## Tools

- **Prometheus**: Metrics collection (`deploy/prod/prometheus/prometheus.yml`).
- **Grafana**: Visualization dashboards (`deploy/prod/grafana/dashboards/api-metrics.json`).
- **Loki**: Log aggregation (`deploy/prod/loki/config.yaml`).
- **Tempo**: Distributed tracing (`deploy/prod/tempo/tempo.yaml`).
- **Vector**: Log processing and routing (`deploy/prod/vector/vector.yaml`).

## Setup

Observability services are defined in `docker-compose.prod.yaml` and activated with the `grafana` profile:

```bash
just up
```

This command activates observability services along with the API and worker containers.

### Service Access

- **Grafana**: http://localhost:3000 (default credentials: admin/admin)
- **Prometheus**: http://localhost:9090 (internal, exposed for debugging)
- **Loki**: http://localhost:3100 (internal, accessed via Grafana)
- **Tempo**: 
  - HTTP API: http://localhost:3200 (internal)
  - gRPC endpoint: http://localhost:4317 (for trace ingestion)
- **Vector**: http://localhost:8383 (internal metrics endpoint)

## Metrics

The Grafana dashboard (`api-metrics.json`) monitors:

- **Total requests**: Overall request count by status code
- **Request counts**: Breakdown by HTTP method and path
- **Average request duration**: Response time statistics
- **Exception counts**: Error tracking and categorization
- **Response percentages**: 2xx, 4xx, 5xx response rate distribution
- **Request latency**: 99th percentile latency measurements
- **Requests per second**: Throughput metrics

Prometheus collects metrics from:
- API service: `pix_erase.api:8080/metrics`
- Worker service: `pix_erase.worker:8081/metrics`

Example Prometheus query:

```promql
sum(fastapi_requests_total{app_name="PixErase", path!="/metrics"}) by (status_code)
```

### Key Metrics

- `fastapi_requests_total`: Total HTTP requests
- `fastapi_request_duration_seconds`: Request duration histogram
- `fastapi_exceptions_total`: Exception counts by type
- `taskiq_tasks_total`: Background task metrics
- `taskiq_tasks_duration_seconds`: Task execution time

## Logs

Loki aggregates logs from the `pix_erase.api` container, processed by Vector for structured log parsing. Logs are viewable in Grafana under the "Log of All FastAPI App" panel.

Vector processes logs with the following structure:
- Parses nested JSON log messages
- Extracts structured fields (log_level, log_event, log_trace_id, etc.)
- Enriches logs with HTTP request metadata
- Routes logs to Loki for storage

Example Loki query:

```logql
{container_name="pix_erase.api"} | json | line_format "{{.log_level}} trace_id={{.log_trace_id}} {{.log_event}}"
```

### Log Fields

- `log_level`: Log severity (DEBUG, INFO, WARNING, ERROR)
- `log_event`: Event description
- `log_trace_id`: OpenTelemetry trace ID for correlation
- `log_span_id`: OpenTelemetry span ID
- `log_http_method`: HTTP method (GET, POST, etc.)
- `log_url`: Request URL path
- `log_status_code`: HTTP response status code
- `log_client_addr`: Client IP address
- `log_timestamp`: Event timestamp

## Tracing

Tempo handles distributed tracing using OpenTelemetry protocol. Traces are automatically correlated with logs via trace IDs, allowing seamless navigation between logs and traces in Grafana.

### Trace Configuration

Traces are sent to Tempo via gRPC at:
- **Endpoint**: `http://${TEMPO_HOST}:${TEMPO_GRPC_PORT}`
- **Protocol**: OTLP gRPC
- **Default**: `http://localhost:4317`

### Tracing Features

- **Automatic instrumentation**: HTTP requests, database queries, and async tasks
- **Custom spans**: Manual span creation for critical operations
- **Trace correlation**: Trace IDs embedded in logs for log-trace correlation
- **Exemplars**: Performance metrics linked to trace spans in Prometheus

View traces in Grafana's Tempo data source or via Tempo's UI at http://localhost:3200.

## Configuration

Key environment variables (`.env.dist`):

### Observability Stack

| Variable           | Description                              | Default   |
|--------------------|------------------------------------------|-----------|
| `GRAFANA_PORT`     | Grafana web UI port                      | `3000`    |
| `GRAFANA_USER`     | Grafana admin username                   | `admin`   |
| `GRAFANA_PASSWORD` | Grafana admin password                   | `admin`   |
| `LOKI_PORT`        | Loki log aggregation service port       | `3100`    |
| `VECTOR_PORT`      | Vector log router/metrics port           | `8383`    |
| `TEMPO_HOST`       | Tempo distributed tracing hostname       | `localhost`|
| `TEMPO_PORT`       | Tempo HTTP API port                      | `3200`    |
| `TEMPO_GRPC_PORT`  | Tempo gRPC endpoint port for traces      | `4317`    |
| `PROMETHEUS_PORT`  | Prometheus metrics collection port       | `9090`    |

### Application Observability

The application name is configured in the codebase (`src/pix_erase/setup/config/obversability.py`):
- **Default app name**: `PixErase`
- **Tempo gRPC URI**: Automatically constructed from `TEMPO_HOST` and `TEMPO_GRPC_PORT`

## Dashboard Access

Once observability services are running:

1. **Open Grafana**: Navigate to http://localhost:3000
2. **Login**: Use default credentials (admin/admin) - change on first login
3. **View Dashboards**: Pre-configured dashboards are automatically provisioned
4. **Explore Logs**: Use Explore tab with Loki data source
5. **View Traces**: Use Explore tab with Tempo data source or dedicated trace views

## Log-Trace Correlation

The observability stack enables seamless correlation between logs and traces:

1. Every log entry includes `trace_id` and `span_id` fields
2. Grafana automatically links logs to traces
3. Click on trace IDs in logs to view full trace details
4. Navigate from traces to related logs via trace ID search