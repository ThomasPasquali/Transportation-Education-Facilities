rm -r ./tmp_df

python3 transport.py
python3 edu.py
python3 users.py

cp -r ./tmp_df ../../Parsed\ data