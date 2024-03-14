#!/usr/bin/env bash

set -euo pipefail

# Function to display usage
usage() {
  echo "Usage: $(basename "$0") [-h] [-f HAR_FILE]"
  echo "Options:"
  echo "  -h, --help       Display this help message"
  echo "  -f, --file FILE  Specify the input HAR file (default: browser_record.har)"
  exit 1
}

# Function to check if the HAR file exists
check_har_file() {
  if [[ ! -f $1 ]]; then
    echo "Error: File '$1' not found"
    exit 1
  fi
}

# Function to convert HAR to Locust file
convert_to_locust() {
  har2locust "$1" > "${SCRIPT_DIR}/../benchmark/generated_locustfile.py"
}

# Parse command-line options
parse_options() {
  while [[ $# -gt 0 ]]; do
    case $1 in
      -h|--help)
        usage
        ;;
      -f|--file)
        if [[ -n $2 ]]; then
          HAR_FILE=$2
          shift
        else
          echo "Error: HAR file not provided after -f option"
          usage
        fi
        ;;
      *)
        echo "Error: Unknown option $1"
        usage
        ;;
    esac
    shift
  done
}

# Main function
main() {
  # Default values
  HAR_FILE=browser_record.har

  # Parse command-line options
  parse_options "$@"

  # Obtain the directory of the script
  SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

  # Check if the HAR file exists
  check_har_file "$HAR_FILE"

  # Convert HAR to Locust file
  convert_to_locust "$HAR_FILE"
}

# Execute main function
main "$@"
