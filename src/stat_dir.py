#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import argparse
import csv
import glob
import sys
import os.path as osp

from sxf_tools.sxf import SXF

SXF_PATH = '../../sample'
OUT_CSV = 'sample.csv'

def main():
  # parser = argparse.ArgumentParser(description='Process dirs.')
  # parser.add_argument('dirs', nargs='+', help='*.sfx files dir or files')
  # parser.add_argument('--out-csv', dest='out_csv', help='output csv [default stdout]')
  # args = parser.parse_args()
  # sxf_path = args.dirs
  # out_csv = args.out_csv
  sxf_path = [SXF_PATH]
  out_csv = OUT_CSV

  fout = open(out_csv, 'w', newline='') if out_csv else sys.stdout
  writerow = csv.writer(fout).writerow
  writerow([
    'ver.SXF', 'Номенклатура', 'Масштаб', 'Название', 'Вид ИКМ', 'Тип ИКМ',
    'К.сумма'])
  for path in walk_args(sxf_path):
    row = get_sxf_info(path)
    writerow(row)

def walk_args(paths):
  for path in paths:
    if not osp.exists(path):
      continue
    if osp.isfile(path):
      yield path
    elif osp.isdir(path):
      yield from glob.iglob(osp.join(path, '*.[Ss][Xx][Ff]'))

def get_sxf_info(path):
  with open(path, 'rb') as f:
    sxf = SXF.parse(f)
    return (
      sxf.version_str, sxf.nomenclatura, sxf.scale, sxf.name,
      sxf.src_kind, sxf.src_type, hex(sxf.crc))

if __name__ == '__main__':
  main()
