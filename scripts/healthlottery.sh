#! /bin/bash

cat /home/danny/Documents/Mail/healthlottery | msmtp -C /home/danny/.msmtprc -a default info@email.healthlottery.co.uk
