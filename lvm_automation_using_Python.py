import os

def lvm_partition():
	IP = input("\t\t\tEnter IP at which you want to create partition:")
	os.system("ssh root@{} fdisk -l".format(IP))
	print("\t\t\tChoose disk for creating physical volume")
	count_pv = input("\t\t\tHow many disk you want to choose for create physical volume: ")
	count_pv = int(count_pv)
	pv=[]
	for i in range(0,count_pv):
		pvname = input("\t\t\tEnter disk {} name:".format(i+1))
		pv.append(pvname)
		print("\t\t\tcreating physical volumes..") 
		os.system("ssh root@{} pvcreate {}".format(IP,pv[i]))
	
		print("\t\t\tdisplaying physical volumes..") 
		os.system("ssh root@{} pvdisplay {}".format(IP,pv[i]))

	vg_name = input("\t\t\tGive the Name of Volume Group:")
	vg_disk = ""
	for i in pv:
		vg_disk = vg_disk + " " + i

	print("\t\t\tCreating volume group..")
	os.system("ssh root@{} vgcreate {} {}".format(IP,vg_name,vg_disk))

	print("\t\t\tDisplaying volume group..")
	os.system("ssh root@{} vgdisplay {}".format(IP,vg_name))

	print("\t\t\tDisplaying physical volumes..")
	for i in pv:
		os.system("ssh root@{} pvdisplay {}".format(IP,i))

	partition_size = input("\t\t\tEnter the partition size you want to create:") 
	lv_name = input("\t\t\tGive Name to logical volume :")

	print("\t\t\tCreating logical volume..")
	os.system("ssh root@{} lvcreate --size {} --name {} {}".format(IP,partition_size,lv_name,vg_name))

	print("\t\t\tDisplaying logical volume..")
	os.system("ssh root@{} lvdisplay /dev/{}/{}".format(IP,vg_name,lv_name))

	print("\t\t\tformat the partition..")
	os.system("ssh root@{} mkfs.ext4 /dev/{}/{}".format(IP,vg_name,lv_name))

	print("\t\t\tmounting partition into folder..")
	mount_folder = input("\t\t\tEnter mount folder name:")

	print("\t\t\tMaking folder for mounting")
	os.system("ssh root@{} mkdir {}".format(IP,mount_folder))

	print("\t\t\tmount the partition..")
	os.system("ssh root@{} mount /dev/{}/{} {}".format(IP,vg_name,lv_name,mount_folder))

	print("\t\t\tshowing status of mounting..")
	os.system("ssh root@{} df -hT".format(IP))

def extend_partition():
	IP = input("\t\t\tEnter IP at which you want to extend partition:")

	lv_extend_name = input("\t\t\tEnter logical volume name which you want to extend the size:")

	extend_size = input("\t\t\tHow many size you want to extend:")

	print("\t\t\textending the size of logical volume..")
	os.system("ssh root@{} lvextend --size +{} {}".format(IP,extend_size,lv_extend_name))

	print("\t\t\tSee the status but not extended in mounted folder because new part not formatted yet..")
	os.system("ssh root@{} df -hT".format(IP))

	print("\t\t\tFormat the new extended space..")
	os.system("ssh root@{} resize2fs {}".format(IP,lv_extend_name))
	
	print("\t\t\tNow mounted folder size also increased.. Check status")
	os.system("ssh root@{} df -hT".format(IP))

def reduce_partition():
	IP = input("\t\t\tEnter IP at which you want to extend partition:")

	lv_reduce_name = input("\t\t\tEnter logical volume name which you want to reduce the size(in GiB):")
	volume_group = input("\t\t\t\tEnter name of volume group: ")
	reduce_size = input("\t\t\tHow many size you want to reduce")
	mounted_folder = input("\t\t\tEnter folder where partition is mounted(full path):")
	print("\t\t\tUnmount the filesystem")
	os.system("ssh root@{} umount {}/".format(IP,mounted_folder))

	print("\t\t\tChecking the filesystem before resizing it.")
	os.system("ssh root@{0} e2fsck -f /dev/{1}/{2}".format(IP,volume_group,lv_reduce_name))

	print("\t\t\tResizing the filesystem")
	os.system("ssh root@{} resize2fs /dev/{}/{} {}G".format(IP,volume_group,lv_reduce_name,reduce_size))

	print("\t\t\tReducing the size of the logical Volume")
	os.system("ssh root@{} lvreduce --size {}G /dev/{}/{} -y".format(IP,reduce_size,volume_group,lv_reduce_name))

	filename = input("\t\t\t\tEnter name of file which you want to mount: ")
	print("\t\t\t Again Mounting ")
	os.system("mount /dev/{}/{} {}".format(volume_group,lv_reduce_name,filename))

	print("\t\t\t See the Status ")
	os.system("ssh root@{} df -hT ".format(IP))

print("\t\t============================================================================")
print("\t\t\t*******Logical Volume Management(LVM) Automation*******\t\t")
print('''\t\t\t\t    Choose one of the option.

	     \t\t\t Option 1: Create logical volume.
	     \t\t\t Option 2: Extend partition size.
		 \t\t Option 3: Reduce partition size.
		 \t\t Option 4: Show all Logical Volumes.''')
print("\t\t============================================================================")
option = input("\t\t\tEnter the option which you want to choose:")
option = int(option)

if(option==1):
	lvm_partition()

elif(option==2):
	extend_partition()

elif(option==3):
	reduce_partition()

elif(option==4):
	IP = input("\t\t\tEnter IP at which you want to extend partition:")
	os.system("ssh root@{} lvdisplay".format(IP))

else:
	print("\n\t\t\tInvalid option!!!")


