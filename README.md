## ติดตั้ง virtualbox

https://www.virtualbox.org/

เซ็ต network ให้เป็น bridge เพื่อให้เราสามารถเข้าถึงเครื่องจำลองได้

## ติดตั้ง Oracle Linux 8.9


---


เตรียม terminal ก่อน 
ติดตั้ง zsh

install ohmyz.sh
[Oh My Zsh - a delightful & open source framework for Zsh](https://ohmyz.sh/#install)

```bash
yum install zsh
```

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
```

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
```


```bash
nano ~/.zshrc
```

หาบรรทัดโค้ดตามนี้ และ ลบ # ออก ก็ถือว่าเราเปิดใช้ ( ลบ comment )
```bash
ENABLE_CORRECTION="true"
```

```bash
plugins=(git
zsh-autosuggestions
zsh-syntax-highlighting
)
```


#ธีมนี้สวย
ZSH_THEME="agnoster"
ธีมเพิ่มเติม
https://github.com/ohmyzsh/ohmyzsh/wiki/Themes

#หาติดตั้งเพิ่มได้
ZSH_THEME="powerlevel10k/powerlevel10k"
วีธีเปลี่ยน style อีกครั้ง
p10k configure

---

## โครงสร้างไฟล์ในวันนี้
```bash
.
├── README.md
├── dump_sql
│   ├── dump_sql.py
│   └── import_sql.py
├── dump_struc
│   ├── dump_struc.py
│   └── import_struc.py
└── linux-commands-cheat-sheet-pdf.pdf

2 directories, 6 files
```


## ติดตั้ง mariadb


```bash
yum install mariadb-server mariadb-devel mariadb-test mariadb-backup -y
```

**รันทีละคำสั่ง**

```bash
sudo systemctl start mariadb
sudo systemctl status mariadb
sudo systemctl enable mariadb
```

**เช็ค version**

```bash
mysql --version
```

**ตั้งค่า mysql secure**

```bash
sudo mysql_secure_installation
```

#### ตัวอย่างการตั้งค่า mysql secure ดูคำตอบ Y หรือ N ตรงไหนบ้าง  !ไม่ต้องก๊อปไปรัน
```bash
Enter current password for root (enter for none):
OK, successfully used password, moving on...

Setting the root password ensures that nobody can log into the MariaDB
root user without the proper authorisation.

Set root password? [Y/n] n
 ... skipping.

By default, a MariaDB installation has an anonymous user, allowing anyone
to log into MariaDB without having to have a user account created for
them.  This is intended only for testing, and to make the installation
go a bit smoother.  You should remove them before moving into a
production environment.

Remove anonymous users? [Y/n] y
 ... Success!

Normally, root should only be allowed to connect from 'localhost'.  This
ensures that someone cannot guess at the root password from the network.

Disallow root login remotely? [Y/n] y
 ... Success!

By default, MariaDB comes with a database named 'test' that anyone can
access.  This is also intended only for testing, and should be removed
before moving into a production environment.

Remove test database and access to it? [Y/n] y
 - Dropping test database...
 ... Success!
 - Removing privileges on test database...
 ... Success!

Reloading the privilege tables will ensure that all changes made so far
will take effect immediately.

Reload privilege tables now? [Y/n] y
 ... Success!

Cleaning up...

All done!  If you've completed all of the above steps, your MariaDB
installation should now be secure.

Thanks for using MariaDB!
```

เข้าไปใน mysql สร้าง user "adminit" 

```bash
mysql -u root -p
```


```bash
CREATE USER 'adminit'@'%' IDENTIFIED BY '123456';
```

```bash
GRANT ALL PRIVILEGES ON *.* TO 'adminit'@'%' WITH GRANT OPTION;

FLUSH PRIVILEGES;
```



## ติดตั้ง python3.9


```bash
sudo dnf module install python39
```

```bash
python3.9 --version
```

### ติดตั้ง progressbar2 และ mysql-connector ของ python3.9

```bash
pip3.9 install progressbar2 mysql-connector
```

**เช็ค package ที่ติดตั้งแล้ว**
```bash
pip3.9 freeze
```

---
## Mysql Dump

a). ดัมโครงสร้างฐานข้อมูลเปล่าๆ
โดย cd เข้าไปที่โฟลเดอร์ dump_struc 

```bash
./dump_struc.py -i <IP_MASTER> -P 3306 -b hos -u <USER> -p <PASSWORD>
```

b). ดัมฐานข้อมูลจริง
cd เข้าไปที่โฟลเดอร์ dump_sql

```bash
./dump_sql.py -i <IP_MASTER> -u <USER> -p <PASSWORD> -P 3306 -b hos -m mysqldump -c true -l true -a false
```

### ปรับ my.cnf ก่อน Import

```bash
innodb_buffer_pool_size = 4G
innodb_log_buffer_size = 256M
innodb_log_file_size = 1G

innodb_write_io_threads = 16        # จำนวน theads
innodb_flush_log_at_trx_commit = 0  # set เป็น 0 เมื่อจะ import ข้อมูล / set เป็น 1 เมื่อ import เสร็จแล้ว
```

## Import to Mysql
ต้องอยู่ในตำแหน่งโฟลเดอร์ที่มีไฟล์ import.py   

*New Options* -t [ --threads ] default 100 threads  
เพิ่ม option ใหม่ -t 100 / 20 / 10 

a). นำเข้าโครงสร้างฐานข้อมูลเปล่าๆ
โดย cd เข้าไปที่โฟลเดอร์ dump_struc 
```bash
./import_struc.py -i <IP_SLAVE> -u <USER> -p <PASSWORD> -P 3306 -b hos -c mysql -t 100 -d ./
```


b). นำเข้าฐานข้อมูลจริง
cd เข้าไปที่โฟลเดอร์ dump_sql

```bash
./import_sql.py -i <IP_SLAVE> -u <USER> -p <PASSWORD> -P 3306 -b hos -c mysql -t 100 -d ./
```



## ปิด selinux

```bash
vim /etc/selinux/config
```

**แก้ไข ในไฟล์เป็น**
```bash
SELINUX=disabled
```

**ออกจาก vim แล้ว รันคำสั่งนี้ที่ command line**

```bash
sudo service firewalld stop
sudo chkconfig firewalld off
```


### คำสั่งค้นหาไฟล์ที่มีขนาดใหญ่กว่า 10M


```bash
mkdir new_folder
find . -type f -size +10M -exec mv "{}" new_folder/ \;
```

## การทำ Mysql replacation   
สิ่งที่ต้องเตรียม   
mysql version ที่แนะนำ mariadb-10.1.xx   
แก้ไข my.cnf โดยใช้คำสั่ง

```bash
nano /etc/my.cnf
```

เพิ่ม config ดังต่อไปนี้
```bash

```