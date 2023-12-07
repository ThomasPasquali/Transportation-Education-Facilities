rm -r ./tmp_df
rm -r ./tmp_df ../../Parsed\ data

python3 1_transport.py & \
python3 2_edu.py & \
python3 3_users.py & \
cp -r ./tmp_df ../../Parsed\ data | \
echo "Something went wrong"