
# Bios DB for MiSTer

This is a Database that will help you get a few console and computer BIOS that are compatible with MiSTer cores.

### How to install

If you use [Update All](https://github.com/theypsilon/Update_All_MiSTer), you may simply activate it there in the Settings Screen.

Alternatively, if you don't use it, you can add an entry to the `update.ini` file on the root of your SD (create it if it doesn't exist), to use it with the [MiSTer Downloader](https://github.com/MiSTer-devel/Downloader_MiSTer/) (which is what Update All calls under the hood). For that, please add the following entry there:

```
[bios_db]
db_url = https://raw.githubusercontent.com/theypsilon/BiosDB_MiSTer/db/bios_db.json
```

Once you've done this, next time you run downloader, the BIOS will get installed too.
