
# need to be root

# prepare directories
echo "Creating directories..."
sudo mkdir -p /backup
sudo chmod 777 /backup
sudo mkdir -p /usr/share/usb-backup

echo "Installing dependencies..."
# install files and dependencies
sudo apt-get install usbmount supervisor
# make usbmount read only
sudo sed -i.bak -r -e '/^MOUNTOPTIONS=\".*ro.*\"/n ; s/(^MOUNTOPTIONS=\")(.*)\"/\1\2,ro\"/g' /etc/usbmount/usbmount.conf

echo "Installing usb-backup files..."
sudo cp supervisor/usb-backup.conf /etc/supervisor/conf.d/usb-backup.conf
sudo cp usb-backup.py /usr/share/usb-backup/usb-backup.py
sudo touch /var/log/usb-backup.log
sudo chmod 666 /var/log/usb-backup.log

echo "Restarting service..."
# restart service
sudo supervisorctl update
sudo supervisorctl restart usb-backup

echo "All done"
