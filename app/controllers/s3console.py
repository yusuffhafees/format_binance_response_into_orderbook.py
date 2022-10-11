import io
from app.tools.encoding_helper import file2str
from app.tools.bytewrite_to_s3 import bytewrite_to_s3
from app.config.s3_upload import BUCKET_NAME, STANDARD_PATH_PARENT




def save_report_in_s3(file_like_object: io.StringIO, file_name: str):
    file_bytes_object = file_like_object.getvalue().encode()
    return bytewrite_to_s3(
        bucket_name=BUCKET_NAME,
        file_path=STANDARD_PATH_PARENT + "/" + file_name,
        content=file2str(file_bytes_object))
    # ), bytewrite_to_s3(
    #     bucket_name=BUCKET_NAME,
    #     file_path=STANDARD_PATH_for_binance + "/" + file_name,
    #     content=file2str(file_bytes_object)), bytewrite_to_s3(
    #     bucket_name=BUCKET_NAME,
    #     file_path=STANDARD_PATH_for_bitvavo + "/" + file_name,
    #     content=file2str(file_bytes_object)),bytewrite_to_s3(
    #     bucket_name=BUCKET_NAME,
    #     file_path=STANDARD_PATH_for_bitstamp + "/" + file_name,
    #     content=file2str(file_bytes_object)), bytewrite_to_s3(
    #     bucket_name=BUCKET_NAME,
    #     file_path=STANDARD_PATH_for_coinbase + "/" + file_name,
    #     content=file2str(file_bytes_object)), bytewrite_to_s3(
    #     bucket_name=BUCKET_NAME,
    #     file_path=STANDARD_PATH_for_bitfinex + "/" + file_name,
    #     content=file2str(file_bytes_object))
