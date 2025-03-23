import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import zipfile

def convert_zipped_csv_to_parquet(zip_path, parquet_path, chunksize=100_000):
    with zipfile.ZipFile(zip_path) as z:
        csv_filename = z.namelist()[0]
        with z.open(csv_filename) as csv_file:
            writer = None
            for chunk in pd.read_csv(csv_file, chunksize=chunksize):
                table = pa.Table.from_pandas(chunk)

                if writer is None:
                    writer = pq.ParquetWriter(parquet_path, table.schema, compression="snappy")

                writer.write_table(table)

            if writer:
                writer.close()

    print(f"✅ Converted to Parquet: {parquet_path}")

# Example usage
zip_path = "Not_to_be_shared_to_repo//Us_Weather_Final_10km_V2.zip"
parquet_path = "Not_to_be_shared_to_repo//Us_Weather_Final_10km_V2.parquet"
convert_zipped_csv_to_parquet(zip_path, parquet_path)
# Output: ✅ Converted to Outputs//DashBoardData.parquet
# The function reads a CSV file from a ZIP archive and writes it to a Parquet file in chunks.