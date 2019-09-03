#!/usr/bin/env bash
rsync -uav --delete xiangf@wrds-cloud.wharton.upenn.edu:/wrdslin/csmar/sasdata/ /home/zigan/Documents/Dataset/wrds/csmar

rsync -uav --delete xiangf@wrds-cloud.wharton.upenn.edu:/wrdslin/levin/sasdata/  /home/zigan/Documents/Dataset/wrds/levin

rsync -uav --delete xiangf@wrds-cloud.wharton.upenn.edu:/wrdslin/etfg/sasdata/  /home/zigan/Documents/Dataset/wrds/etfg

rsync -uav --delete xiangf@wrds-cloud.wharton.upenn.edu:/wrdslin/fisd/sasdata/  /home/zigan/Documents/Dataset/wrds/fisd

rsync -uav --delete xiangf@wrds-cloud.wharton.upenn.edu:/wrdslin/markit/sasdata/ /home/zigan/Documents/Dataset/wrds/markit

rsync -uav --delete xiangf@wrds-cloud.wharton.upenn.edu:/wrdslin/boardex/sasdata/ /home/zigan/Documents/Dataset/wrds/boardex

rsync -uav --delete xiangf@wrds-cloud.wharton.upenn.edu:/wrdslin/factset/sasdata/ /home/zigan/Documents/Dataset/wrds/factset
