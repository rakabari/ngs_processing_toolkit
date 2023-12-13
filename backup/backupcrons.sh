# Daily Backup at 2 AM
0 2 * * * rsync -av --exclude-from={exclude_list} {src} {daily}

# Weekly Backup on Sundays at 3 AM
0 3 * * 0 rsync -av --exclude-from={exclude_list} {src} {weekly}

# Monthly Backup on the 1st day of the month at 4 AM
0 4 1 * * rsync -av --exclude-from={exclude_list} {src} {monthly}

# Quarterly Backup on the 1st day of Jan, Apr, Jul, and Oct at 5 AM
0 5 1 1,4,7,10 * rsync -av --exclude-from={exclude_list} {src} {quarterly}

# Yearly Backup on January 1st at 6 AM
0 6 1 1 * rsync -av --exclude-from={exclude_list} {src} {yearly}

