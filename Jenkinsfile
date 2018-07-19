pipeline {
  agent any
  stages {
    stage('Build openWRT') {
      parallel {
        stage('Build openWRT') {
          steps {
            sh '''ls -al
whoami'''
            echo 'Compile openWRT'
          }
        }
        stage('CPPCheck') {
          steps {
            sh 'cppcheck  mtk-openwrt-4.0.1.0'
          }
        }
        stage('Build openWRT') {
          steps {
            sh './build.sh openwrt'
          }
        }
      }
    }
    stage('Test openWRT') {
      steps {
        echo 'TEST TODO'
        sh 'ls -al'
      }
    }
    stage('Notification openWRT') {
      parallel {
        stage('Notification openWRT') {
          steps {
            slackSend(message: '[Compile Done] openWRT', baseUrl: 'https://withusplanet.slack.com/services/hooks/jenkins-ci/', token: 'fO9IZpUz2PuTiTzUxZh63YH6', failOnError: true, color: 'Red')
          }
        }
        stage('Copy Image to tftpboot') {
          steps {
            sh '''whoami 
ls -al mtk-openwrt-4.0.1.0/bin/targets/mediatek/mt7622-glibc'''
            sh 'sudo cp mtk-openwrt-4.0.1.0/bin/targets/mediatek/mt7622-glibc/lede-mediatek-mt7622-MTK-AC2600-RFB1-squashfs-sysupgrade.bin /tftpboot/lede-mediatek-mt7622-MTK-AC2600-RFB1-squashfs-sysupgrade.bin'
          }
        }
        stage('Send Image to Server') {
          steps {
            sshPublisher(masterNodeName: 'hepark@192.168.1.166', publishers: [ sshPublisherDesc(configName: 'hepark@192.168.1.166',		    		transfers: [										sshTransfer(										sourceFiles: 'openmtk4010/mtk-openwrt-4.0.1.0/bin/targets/mediatek/mt7622-glibc/lede-mediatek-mt7622-MTK-AC2600-RFB1-squashfs-sysupgrade.bin',						removePrefix: 'openmtk4010/mtk-openwrt-4.0.1.0/bin/targets/mediatek/mt7622-glibc',                        			remoteDirectory: '/home/hepark/release',                        				execCommand: 'scp mtk-openwrt-4.0.1.0/bin/targets/mediatek/mt7622-glibc/lede-mediatek-mt7622-MTK-AC2600-RFB1-squashfs-sysupgrade.bin /home/hepark/release/lede-mediatek-mt7622-MTK-AC2600-RFB1-squashfs-sysupgrade.bin'											)		    								]		  							)	        								 ])
          }
        }
      }
    }
  }
}