 
d = 10551358
a=b=c=e = 0
'''
    e = 1
main_loop:
    c = 1
sub_loop:
    b = e * c
    if b == d:
      a = a + e
    c += 1        
    if c <= d:
      goto sub_loop
    e += 1
    if e > d:
      goto end
    goto main_loop
end:
'''

e = 1
while e <= d:
  c = 1
  while c <= d:
    b = e * c
    if b == d:
      a += e
    c += 1
  e += 1

print(a)