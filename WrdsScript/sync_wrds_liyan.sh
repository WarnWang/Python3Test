#!/usr/bin/env bash

rsync -uav --delete xiangf@wrds-cloud.wharton.upenn.edu:/wrdslin/levin/sasdata/  /home/zigan/Documents/Dataset/wrds/levin

rsync -uav --delete xiangf@wrds-cloud.wharton.upenn.edu:/wrdslin/etfg/sasdata/  /home/zigan/Documents/Dataset/wrds/etfg

rsync -uav --delete xiangf@wrds-cloud.wharton.upenn.edu:/wrdslin/fisd/sasdata/  /home/zigan/Documents/Dataset/wrds/fisd

rsync -uav --delete xiangf@wrds-cloud.wharton.upenn.edu:/wrdslin/markit/sasdata/ /home/zigan/Documents/Dataset/wrds/markit
