data "archive_file" "ingester_lambda" {
    type = "zip"
    source_file = "${path.module}/../src/ingester/ingester.py"
    output_path = "${path.module}/../src/ingester/ingester_payload.zip"
}


data "archive_file" "ingester_utils" {
    type = "zip"
    source_dir = "${path.module}/../src/ingester/utils"
    output_path = "${path.module}/../src/ingester/utils_payload.zip"
}