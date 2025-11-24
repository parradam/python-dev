# Ensure UTF-8 encoding for Out-File
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'

# Timestamp for artifacts
$timestamp = Get-Date -Format "yyyyMMddHHmmss"

# Start build log
Write-Output "#################### Build Started: $(Get-Date) ##############################" > .\build.log

# Build image from Dockerfile via docker compose
try {
    docker compose up -d --no-deps --build
} catch {
    Write-Output "Docker build failed: $_" >> .\build.log
    exit 1
}

Write-Output "#################### Build Finished: $(Get-Date) ##############################" >> .\build.log

# Get image ID by repository/tag (safer than first image)
$imageid = docker images python-dev-log:latest --format "{{.ID}}"
if (-not $imageid) {
    # fallback: grab most recent image
    $imageid = docker images --format "{{.ID}}" | Select-Object -First 1
}

Write-Output "ImageID: $imageid" >> .\build.log

# Get latest container ID
$containerid = docker ps -l -q
Write-Output "ContainerID: $containerid" >> .\build.log

# Tag and save image with timestamped tarball
Write-Output "##################### Starting Image:$imageid Save: $(Get-Date) ##############################" >> .\build.log
docker image tag $imageid python-dev-log:latest
docker save -o "pydev-$timestamp.tar" $imageid
Write-Output "##################### Finished Image:$imageid Save: $(Get-Date) ##############################" >> .\build.log

# Docker Scout scan
Write-Output "##################### Starting Image:$imageid Scan: $(Get-Date) ##############################" >> .\build.log

# Get Docker Scout version (last line only)
(docker scout version | Select-Object -Last 1) >> .\build.log

# Run filtered scan first
$scanOutput = docker scout cves python-dev-log:latest

# Save full CVE details separately
$fullReportFile = ".\cves-full-$timestamp.txt"
$scanOutput | Out-File -FilePath $fullReportFile -Encoding utf8

# Append Scout's own summary (last lines) to build.log
$summaryLines = Get-Content $fullReportFile | Select-Object -Last 10
Write-Output "CVE Summary (from Docker Scout):" >> .\build.log
$summaryLines | Out-File -FilePath .\build.log -Append -Encoding utf8

Write-Output "##################### Finished Image Scan: $(Get-Date) ##############################" >> .\build.log

# Optional cleanup (uncomment if desired)
# docker builder prune -f
