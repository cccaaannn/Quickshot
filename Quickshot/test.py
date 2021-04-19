from ss_handler import ss_handler

ss_handler = ss_handler(default_screen=2)
# is_ss_ok, ss_info = ss_handler.take_ss(ss_bbox=(50,50,500,500))
is_ss_ok, ss_info = ss_handler.take_ss()

if(is_ss_ok):
    print("ss saved to:", ss_info)
else:
    print(ss_info)