# source

Description:
```
I store all my secrets in binaries, no one can read them if they don't have the source code!
```

We know a that hardcoded strings will be visible in the binary file.

We can run strings on the binary. To see if we can find the secrets.
```bash
strings main|grep {

TFC{3v3ryth1ng_1s_0p3n_5ourc3_1f_y0u try_h4rd_3n0ugh}
```

