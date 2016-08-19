# Glacier Backup

This program builds on Amazon's own boto3 library for enabling backups to Amazon Glacier, while also maintaining a local, rotated copy using the excellent archive-rotator package to implement the generalized grandfather-father-son rotation methodology. Single files or directories are accepted, where directories are recursively tar'ed and compression is optional via the lzma xz format, which has excellent compression ratio and fast decompression speed.

## Usage

The script is intended to run on a periodic basis via cron, [systemd timers](https://wiki.archlinux.org/index.php/Systemd/Timers), or any other scheduling mechanism. It is intended to run daily, and will keep local copies for 7 days, 4 weeks, and 12 months (technically, 4 7-day intervals and 12 4-week intervals). However, you can run it more often, just be aware that if you set it up eg. hourly, then the second tier of updates will be 7 hour intervals, and the third will be 4 7-hour intervals. In the future this may become configurable via commandline flags. Feel free to pull request.

Here is an example invocation with cron executing every day at 1am, archiving and compressing the `/var/www/example.com` directory and saving it locally in `/backups/` under rotation. You can use [crontab-generator.org](http://crontab-generator.org/) to generate other configurations.

    0 1 * * * /usr/local/glacer-backup --compress /var/www/example.com /backups/


You can use `glacier-backup --help` to view the options available to you.
