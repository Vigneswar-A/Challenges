from string import ascii_letters as letters
flag = "flag{Y0u_c4n_3v4l_n1ce}"
eval(expr if (len(expr := input("Enter a math expression: ")) <= 8 and all(c.lower() not in letters for c in expr)) else 'print("Can\'t compute that much!")')
