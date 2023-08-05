import glob
import re
import mock

from os import path
from iml_common.blockdevices.blockdevice_zfs import BlockDeviceZfs, ZfsDevice, ZFS_OBJECT_STORE_PATH
from tests.blockdevices.blockdevice_base_tests import BaseTestBD
from tests.data import example_data
from iml_common.test.command_capture_testcase import CommandCaptureCommand


class TestBlockDeviceZfs(BaseTestBD.BaseTestBlockDevice):
    pool_name = 'zfs_pool_devdiskbyidscsi0QEMU_QEMU_HARDDISK_WDWMAP3333333'
    dataset_path = '/'.join([pool_name, 'ost_index0'])

    rpm_qi_zfs_stdout = """Name        : zfs
Version     : 0.6.5.7
Release     : 1.el7
Architecture: x86_64
Install Date: Wed 05 Oct 2016 07:59:50 PDT
Group       : System Environment/Kernel
Size        : 819698
License     : CDDL
Signature   : (none)
Source RPM  : zfs-0.6.5.7-1.el7.src.rpm
Build Date  : Sat 20 Aug 2016 09:34:50 PDT
Build Host  : onyx-1-sdg1-el7-x8664.onyx.hpdd.intel.com
Relocations : (not relocatable)
URL         : http://zfsonlinux.org/
Summary     : Commands to control the kernel modules and libraries
Description :
This package contains the ZFS command line utilities.
"""

    rpm_qi_spl_stdout = """[root@lotus-33vm18 ~]# rpm -qi spl
Name        : spl
Version     : 1.2.3.4
Release     : 1.el7
Architecture: x86_64
Install Date: Wed 05 Oct 2016 08:35:27 PDT
Group       : System Environment/Kernel
Size        : 49120
License     : GPLv2+
Signature   : (none)
Source RPM  : spl-0.6.5.7-1.el7.src.rpm
Build Date  : Sat 20 Aug 2016 09:31:43 PDT
Build Host  : onyx-1-sdg1-el7-x8664.onyx.hpdd.intel.com
Relocations : (not relocatable)
URL         : http://zfsonlinux.org/
Summary     : Commands to control the kernel modules
Description :
This package contains the commands to verify the SPL
kernel modules are functioning properly.
"""

    zpool_properties = '-\tsize\t68G\t-\n' \
                       '-\thealth\tONLINE\t-\n' \
                       '-\tcachefile\t-\t-\n' \
                       '-\treadonly\toff\t-\n'
    zpool_properties_readonly = '-\tsize\t68G\t-\n' \
                                '-\thealth\tONLINE\t-\n' \
                                '-\tcachefile\t-\t-\n' \
                                '-\treadonly\ton\t-\n'

    def setUp(self):
        super(TestBlockDeviceZfs, self).setUp()

        self.mock_makedirs = mock.Mock()
        self.mock_remove = mock.Mock()
        mock.patch('iml_common.blockdevices.blockdevice_zfs.ZfsDevice.lock_pool').start()
        mock.patch('iml_common.blockdevices.blockdevice_zfs.ZfsDevice.unlock_pool').start()
        mock.patch('os.makedirs', self.mock_makedirs).start()
        mock.patch('os.remove', self.mock_remove).start()
        self.patch_init_modules = mock.patch.object(BlockDeviceZfs, '_initialize_modules')
        self.patch_init_modules.start()
        self.mock_open = mock.mock_open()
        mock.patch('__builtin__.open', self.mock_open, create=True).start()

        self.blockdevice = BlockDeviceZfs('zfs', self.pool_name)

        self.reset_command_capture()
        self.reset_command_capture_logs()
        self.addCleanup(mock.patch.stopall)

    def test_initialize_modules(self):
        self.patch_init_modules.stop()

        self.add_commands(CommandCaptureCommand(('modprobe', 'osd_zfs')),
                          CommandCaptureCommand(('modprobe', 'zfs')))

        self.blockdevice._initialize_modules()
        self.assertTrue(self.blockdevice._modules_initialized)

        self.assertRanAllCommandsInOrder()

    def test_filesystem_type_unoccupied(self):
        # this should be called with device_path referencing a zpool
        self.add_command(('zfs', 'list', '-H', '-o', 'name', '-r', self.blockdevice._device_path),
                         stdout=self.blockdevice._device_path)

        self.assertEqual(None, self.blockdevice.filesystem_type)
        self.assertRanAllCommandsInOrder()

    def test_filesystem_type_occupied(self):
        # this should be called with device_path referencing a zpool
        self.add_command(('zfs', 'list', '-H', '-o', 'name', '-r', self.blockdevice._device_path),
                         stdout='%(pool)s\n%(pool)s/dataset_1' % {'pool': self.blockdevice._device_path})

        self.assertEqual('zfs', self.blockdevice.filesystem_type)
        self.assertRanAllCommandsInOrder()

    def test_filesystem_info_unoccupied(self):
        # this should be called with device_path referencing a zpool
        self.add_command(('zfs', 'list', '-H', '-o', 'name', '-r', self.blockdevice._device_path),
                         stdout=self.blockdevice._device_path)

        self.assertEqual(None, self.blockdevice.filesystem_info)
        self.assertRanAllCommandsInOrder()

    def test_filesystem_info_occupied(self):
        # this should be called with device_path referencing a zpool
        self.add_command(('zfs', 'list', '-H', '-o', 'name', '-r', self.blockdevice._device_path),
                         stdout='%(pool)s\n%(pool)s/dataset_1' % {'pool': self.blockdevice._device_path})

        self.assertEqual("Dataset 'dataset_1' found on zpool '%s'" %
                         self.blockdevice._device_path, self.blockdevice.filesystem_info)
        self.assertRanAllCommandsInOrder()

    def test_filesystem_info_occupied_multiple(self):
        # this should be called with device_path referencing a zpool
        self.add_command(('zfs', 'list', '-H', '-o', 'name', '-r', self.blockdevice._device_path),
                         stdout='%(pool)s\n%(pool)s/dataset_1\n%(pool)s/dataset_2' % {'pool':
                                                                                      self.blockdevice._device_path})

        self.assertEqual("Datasets 'dataset_1,dataset_2' found on zpool '%s'" %
                         self.blockdevice._device_path, self.blockdevice.filesystem_info)
        self.assertRanAllCommandsInOrder()

    def test_uuid(self):
        self.add_commands(CommandCaptureCommand(('zpool', 'list', '-H', '-o', 'name'),
                                                stdout=self.blockdevice._device_path),
                          CommandCaptureCommand(('zfs', 'get', '-H', '-o', 'value', 'guid', self.blockdevice._device_path),
                                                stdout='169883839435093209\n'))

        self.assertEqual('169883839435093209', self.blockdevice.uuid)
        self.assertRanAllCommandsInOrder()

    def test_preferred_fstype(self):
        self.assertEqual('zfs', self.blockdevice.preferred_fstype)

    def test_device_type(self):
        self.assertEqual('zfs', self.blockdevice.device_type)

    def test_device_path(self):
        self.assertEqual(self.pool_name, self.blockdevice._device_path)

    def test_mgs_targets(self):
        self.assertEqual({}, self.blockdevice.mgs_targets(None))

    def test_import_success_non_pacemaker(self):
        self.blockdevice = BlockDeviceZfs('zfs', self.dataset_path)

        self.add_commands(CommandCaptureCommand(('zpool', 'import', self.pool_name)))

        self.assertIsNone(self.blockdevice.import_(False))
        self.assertRanAllCommandsInOrder()

    def test_import_existing_readonly(self):
        props = re.sub(r'readonly\s+off', 'readonly    on', example_data.zpool_example_properties)

        self.add_commands(CommandCaptureCommand(('zpool', 'import', self.pool_name),
                                                rc=1,
                                                stderr="cannot import '%s': a pool with that name already exists\n"
                                                       "use the form 'zpool import <pool | id> <newpool>' to give it "
                                                       "a new name\n",
                                                executions_remaining=1),
                          CommandCaptureCommand(('zpool', 'list', '-H', '-o', 'name'),
                                                stdout='%s\n' % self.pool_name),
                          CommandCaptureCommand(('zpool', 'get', '-Hp', 'all', self.pool_name),
                                                stdout=props,
                                                executions_remaining=1),
                          CommandCaptureCommand(('zpool', 'export', self.pool_name)),
                          CommandCaptureCommand(('zpool', 'import', self.pool_name),
                                                executions_remaining=1),
                          CommandCaptureCommand(('zpool', 'list', '-H', '-o', 'name'),
                                                stdout='%s\n' % self.pool_name),
                          CommandCaptureCommand(('zpool', 'get', '-Hp', 'all', self.pool_name),
                                                stdout=example_data.zpool_example_properties))

        self.blockdevice = BlockDeviceZfs('zfs', self.dataset_path)

        self.assertIsNone(self.blockdevice.import_(False))
        self.assertRanAllCommandsInOrder()

    def test_import_success_with_pacemaker(self):
        self.blockdevice = BlockDeviceZfs('zfs', self.dataset_path)

        self.add_commands(CommandCaptureCommand(('zpool', 'import', '-f', self.blockdevice._device_path.split('/')[0])))

        self.assertIsNone(self.blockdevice.import_(True))
        self.assertRanAllCommandsInOrder()

    def test_import_existing_non_pacemaker(self):
        self.blockdevice = BlockDeviceZfs('zfs', self.dataset_path)

        self.add_commands(CommandCaptureCommand(('zpool', 'import', self.pool_name)))

        self.assertIsNone(self.blockdevice.import_(False))
        self.assertRanAllCommandsInOrder()

    def test_import_existing_with_pacemaker(self):
        self.test_import_existing_non_pacemaker()

    def test_export_success(self):
        self.blockdevice = BlockDeviceZfs('zfs', self.dataset_path)

        self.add_command(('zpool', 'export', self.pool_name))

        self.assertIsNone(self.blockdevice.export())
        self.assertRanAllCommandsInOrder()

    def test_export_missing(self):
        self.blockdevice = BlockDeviceZfs('zfs', self.dataset_path)

        self.add_command(('zpool', 'export', self.pool_name))

        self.assertIsNone(self.blockdevice.export())
        self.assertRanAllCommandsInOrder()

    def test_property_values(self):
        self.blockdevice = BlockDeviceZfs('zfs', self.dataset_path)

        self.add_commands(CommandCaptureCommand(('zpool', 'list', '-H', '-o', 'name'),
                                                stdout='%s\n' % self.pool_name),
                          CommandCaptureCommand(('zfs', 'get', '-Hp', '-o', 'property,value', 'all', self.blockdevice._device_path),
                                                stdout=example_data.zfs_example_properties))

        zfs_properties = self.blockdevice.zfs_properties(False)

        self.assertEqual(zfs_properties['lustre:fsname'], 'efs')
        self.assertEqual(zfs_properties['lustre:svname'], 'efs-MDT0000')
        self.assertEqual(zfs_properties['lustre:flags'], '37')
        self.assertRanAllCommandsInOrder()

    def test_targets(self):
        self.blockdevice = BlockDeviceZfs('zfs', self.dataset_path)

        self.add_commands(CommandCaptureCommand(('zpool', 'list', '-H', '-o', 'name'),
                                                stdout='%s\n' % self.pool_name),
                          CommandCaptureCommand(('zfs', 'get', '-Hp', '-o', 'property,value', 'all', self.blockdevice._device_path),
                                                stdout=example_data.zfs_example_properties))

        target_info = self.blockdevice.targets(None, None, None)

        self.assertIn('efs-MDT0000', target_info.names)
        self.assertEqual(target_info.params['fsname'], ['efs'])
        self.assertEqual(target_info.params['svname'], ['efs-MDT0000'])
        self.assertEqual(target_info.params['flags'], ['37'])
        self.assertRanAllCommandsInOrder()

    def test_purge_filesystem_information(self):
        self.blockdevice = BlockDeviceZfs('zfs', self.dataset_path)

        self.add_commands(CommandCaptureCommand(('lctl', 'erase_lcfg', 'testfs')))

        with mock.patch.object(glob, 'glob', return_value=['testfs-a', 'testfs-b']):
            result = self.blockdevice.purge_filesystem_configuration('testfs', None)

        self.assertEqual(result, None)
        self.assertRanAllCommandsInOrder()

    def test_initialise_driver(self):
        self.add_commands(CommandCaptureCommand(('genhostid',)),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs.target')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs.target')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-import-scan')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-import-scan')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-import-cache')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-import-cache')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-mount')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-mount')),
                          CommandCaptureCommand(('rpm', '-qi', 'spl'), stdout=self.rpm_qi_spl_stdout),
                          CommandCaptureCommand(('dkms', 'install', 'spl/1.2.3.4')),
                          CommandCaptureCommand(('modprobe', 'spl')),
                          CommandCaptureCommand(('rpm', '-qi', 'zfs'), stdout=self.rpm_qi_zfs_stdout),
                          CommandCaptureCommand(('dkms', 'install', 'zfs/0.6.5.7')),
                          CommandCaptureCommand(('modprobe', 'zfs')))

        with mock.patch.object(path, 'isfile', return_value=False):
            result = BlockDeviceZfs.initialise_driver(True)

        self.mock_makedirs.assert_called_once_with(ZfsDevice.ZPOOL_LOCK_DIR)
        self.mock_open.assert_called_once_with(ZFS_OBJECT_STORE_PATH, 'a')
        self.assertEqual(result, None)
        self.assertRanAllCommandsInOrder()

    def test_initialise_driver_file_exists(self):
        self.add_commands(CommandCaptureCommand(('systemctl', 'status', 'zfs.target')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs.target')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-import-scan')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-import-scan')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-import-cache')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-import-cache')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-mount')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-mount')),
                          CommandCaptureCommand(('rpm', '-qi', 'spl'), stdout=self.rpm_qi_spl_stdout),
                          CommandCaptureCommand(('dkms', 'install', 'spl/1.2.3.4')),
                          CommandCaptureCommand(('modprobe', 'spl')),
                          CommandCaptureCommand(('rpm', '-qi', 'zfs'), stdout=self.rpm_qi_zfs_stdout),
                          CommandCaptureCommand(('dkms', 'install', 'zfs/0.6.5.7')),
                          CommandCaptureCommand(('modprobe', 'zfs')))

        with mock.patch.object(path, 'isfile', return_value=True):
            result = BlockDeviceZfs.initialise_driver(True)

        self.mock_makedirs.assert_called_once_with(ZfsDevice.ZPOOL_LOCK_DIR)
        self.mock_open.assert_called_once_with(ZFS_OBJECT_STORE_PATH, 'a')
        self.assertEqual(result, None)
        self.assertRanAllCommandsInOrder()

    def test_initialise_driver_fail_genhostid(self):
        self.add_commands(CommandCaptureCommand(('genhostid',), rc=1, stderr='sample genhostid error text'))

        with mock.patch.object(path, 'isfile', return_value=False):
            result = BlockDeviceZfs.initialise_driver(True)

        self.mock_makedirs.assert_called_once_with(ZfsDevice.ZPOOL_LOCK_DIR)
        self.mock_open.assert_called_once_with(ZFS_OBJECT_STORE_PATH, 'a')
        self.assertIn('sample genhostid error text', result)
        self.assertRanAllCommandsInOrder()

    def test_initialise_driver_fail_dkms_spl(self):
        self.add_commands(CommandCaptureCommand(('genhostid',)),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs.target')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs.target')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-import-scan')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-import-scan')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-import-cache')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-import-cache')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-mount')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-mount')),
                          CommandCaptureCommand(('rpm', '-qi', 'spl'), stdout=self.rpm_qi_spl_stdout),
                          CommandCaptureCommand(('dkms', 'install', 'spl/1.2.3.4'), rc=1, stderr='sample dkms error text'))

        with mock.patch.object(path, 'isfile', return_value=False):
            result = BlockDeviceZfs.initialise_driver(True)

        self.mock_makedirs.assert_called_once_with(ZfsDevice.ZPOOL_LOCK_DIR)
        self.mock_open.assert_called_once_with(ZFS_OBJECT_STORE_PATH, 'a')
        self.assertIn('sample dkms error text', result)
        self.assertRanAllCommandsInOrder()

    def test_initialise_driver_fail_dkms_zfs(self):
        self.add_commands(CommandCaptureCommand(('genhostid',)),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs.target')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs.target')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-import-scan')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-import-scan')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-import-cache')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-import-cache')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-mount')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-mount')),
                          CommandCaptureCommand(('rpm', '-qi', 'spl'), stdout=self.rpm_qi_spl_stdout),
                          CommandCaptureCommand(('dkms', 'install', 'spl/1.2.3.4')),
                          CommandCaptureCommand(('modprobe', 'spl')),
                          CommandCaptureCommand(('rpm', '-qi', 'zfs'), stdout=self.rpm_qi_zfs_stdout),
                          CommandCaptureCommand(('dkms', 'install', 'zfs/0.6.5.7'), rc=1, stderr='sample dkms error text'))

        with mock.patch.object(path, 'isfile', return_value=False):
            result = BlockDeviceZfs.initialise_driver(True)

        self.mock_makedirs.assert_called_once_with(ZfsDevice.ZPOOL_LOCK_DIR)
        self.mock_open.assert_called_once_with(ZFS_OBJECT_STORE_PATH, 'a')
        self.assertIn('sample dkms error text', result)
        self.assertRanAllCommandsInOrder()

    def test_initialise_driver_fail_modprobe_zfs(self):
        self.add_commands(CommandCaptureCommand(('genhostid',)),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs.target')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs.target')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-import-scan')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-import-scan')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-import-cache')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-import-cache')),
                          CommandCaptureCommand(('systemctl', 'status', 'zfs-mount')),
                          CommandCaptureCommand(('systemctl', 'disable', 'zfs-mount')),
                          CommandCaptureCommand(('rpm', '-qi', 'spl'), stdout=self.rpm_qi_spl_stdout),
                          CommandCaptureCommand(('dkms', 'install', 'spl/1.2.3.4')),
                          CommandCaptureCommand(('modprobe', 'spl')),
                          CommandCaptureCommand(('rpm', '-qi', 'zfs'), stdout=self.rpm_qi_zfs_stdout),
                          CommandCaptureCommand(('dkms', 'install', 'zfs/0.6.5.7')),
                          CommandCaptureCommand(('modprobe', 'zfs'), rc=1, stderr='sample modprobe error text'))

        with mock.patch.object(path, 'isfile', return_value=False):
            result = BlockDeviceZfs.initialise_driver(True)

        self.mock_makedirs.assert_called_once_with(ZfsDevice.ZPOOL_LOCK_DIR)
        self.mock_open.assert_called_once_with(ZFS_OBJECT_STORE_PATH, 'a')
        self.assertIn('sample modprobe error text', result)
        self.assertRanAllCommandsInOrder()

    def test_initialise_driver_monitor_mode(self):
        result = BlockDeviceZfs.initialise_driver(False)

        self.mock_makedirs.assert_called_once_with(ZfsDevice.ZPOOL_LOCK_DIR)
        self.mock_open.assert_called_once_with(ZFS_OBJECT_STORE_PATH, 'a')
        self.assertEqual(result, None)
        self.assertRanAllCommandsInOrder()

    def _base_terminate_driver_test(self, getpid_retval, listdir_retval, lockfilepid_retval):
        mock_getpid = mock.Mock(return_value=getpid_retval)
        mock.patch('os.getpid', mock_getpid).start()
        mock_listdir = mock.Mock(return_value=listdir_retval)
        mock.patch('os.listdir', mock_listdir).start()
        mock_lockfilepid = mock.Mock(return_value=lockfilepid_retval)
        mock.patch('iml_common.blockdevices.blockdevice_zfs.get_lockfile_pid', mock_lockfilepid).start()

        result = BlockDeviceZfs.terminate_driver()

        self.assertEqual(result, None)

        return mock_getpid, mock_listdir, mock_lockfilepid

    def test_terminate_driver_active_locks_this_process(self):
        mock_getpid, mock_listdir, mock_lockfilepid = self._base_terminate_driver_test(1234,
                                                                                                    ['pool1'],
                                                                                                    1234)
        mock_getpid.assert_called_once_with()
        mock_listdir.assert_called_once_with(ZfsDevice.ZPOOL_LOCK_DIR)
        mock_lockfilepid.assert_called_once_with('%s/pool1' % ZfsDevice.ZPOOL_LOCK_DIR)
        self.mock_remove.assert_called_once_with('%s/pool1' % ZfsDevice.ZPOOL_LOCK_DIR)

    def test_terminate_driver_active_locks_other_process(self):
        mock_getpid, mock_listdir, mock_lockfilepid = self._base_terminate_driver_test(1233,
                                                                                                    ['pool1'],
                                                                                                    1234)
        mock_getpid.assert_called_once_with()
        mock_listdir.assert_called_once_with(ZfsDevice.ZPOOL_LOCK_DIR)
        mock_lockfilepid.assert_called_once_with('%s/pool1' % ZfsDevice.ZPOOL_LOCK_DIR)
        self.mock_remove.assert_not_called()

    def test_terminate_driver_file_with_no_pid(self):
        mock_getpid = mock.Mock(return_value=1234)
        mock.patch('os.getpid', mock_getpid).start()
        mock_listdir = mock.Mock(return_value=['pool1'])
        mock.patch('os.listdir', mock_listdir).start()
        mock_lockfilepid = mock.Mock(side_effect=AssertionError)
        mock.patch('iml_common.blockdevices.blockdevice_zfs.get_lockfile_pid', mock_lockfilepid).start()

        result = BlockDeviceZfs.terminate_driver()

        self.assertEqual(result, None)

        assert mock_getpid.call_args_list == []
        mock_listdir.assert_called_once_with(ZfsDevice.ZPOOL_LOCK_DIR)
        mock_lockfilepid.assert_called_once_with('%s/pool1' % ZfsDevice.ZPOOL_LOCK_DIR)
        self.mock_remove.assert_not_called()
