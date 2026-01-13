# Exit on error
$ErrorActionPreference = "Stop"

# Hardcoded branch name
$BranchName = "latest_branch"

# Calculate repository size excluding .venv
Write-Host "calculating repository size (excluding .venv)..."

$repoBytes = Get-ChildItem -Recurse -File |
    Where-Object { $_.FullName -notmatch '\\\.venv\\' } |
    Measure-Object -Property Length -Sum |
    Select-Object -ExpandProperty Sum

function Format-Size($bytes) {
    if ($bytes -ge 1GB) {
        return "{0:N2} GB" -f ($bytes / 1GB)
    }
    elseif ($bytes -ge 1KB) {
        return "{0:N2} KB" -f ($bytes / 1KB)
    }
    else {
        return "$bytes bytes"
    }
}

$FormattedSize = Format-Size $repoBytes
$CommitMessage = "done reset git repo of $FormattedSize of data"

Write-Host "repo size detected: $FormattedSize"

# Create orphan branch
Write-Host "creating orphan branch: $BranchName"
git checkout --orphan $BranchName

# Add and commit all files
Write-Host "adding and committing files to $BranchName"
git add -A
git commit -m $CommitMessage

# Delete main branch if exists
if (git branch --list main) {
    Write-Host "deleting main branch"
    git branch -D main
}

# Rename orphan branch to main
Write-Host "renaming branch $BranchName to main"
git branch -m main

# Force push
Write-Host "force pushing changes to remote"
git push -f origin main

Write-Host "done reset git repo"
