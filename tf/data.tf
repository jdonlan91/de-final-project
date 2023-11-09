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


data "archive_file" "processor_lambda" {
    type = "zip"
    source_file = "${path.module}/../src/processor/processor.py"
    output_path = "${path.module}/../src/processor/processor_payload.zip"
}


data "archive_file" "processor_utils" {
    type = "zip"
    source_dir = "${path.module}/../temp/processor-utils"
    output_path = "${path.module}/../src/processor/utils_payload.zip"
}


data "archive_file" "loader_lambda" {
    type = "zip"
    source_file = "${path.module}/../src/loader/loader.py"
    output_path = "${path.module}/../src/loader/loader_payload.zip"
}


data "archive_file" "loader_utils" {
    type = "zip"
    source_dir = "${path.module}/../temp/loader-utils"
    output_path = "${path.module}/../src/loader/utils_payload.zip"
}

