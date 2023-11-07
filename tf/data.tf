data "archive_file" "ingestor_lambda" {
    type = "zip"
    source_file = "${path.module}/../src/ingestor/ingestor.py"
    output_path = "${path.module}/../src/ingestor/ingestor_payload.zip"
}


data "archive_file" "ingestor_utils" {
    type = "zip"
    source_dir = "${path.module}/../temp/ingestor-utils"
    output_path = "${path.module}/../src/ingestor/utils_payload.zip"
}

