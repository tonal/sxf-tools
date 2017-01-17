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

def main():
  parser = argparse.ArgumentParser(description='Process dirs.')
  parser.add_argument('dirs', nargs='+', help='*.sfx files dir or files')
  parser.add_argument('--out-csv', dest='out_csv', help='output csv [default stdout]')
  args = parser.parse_args()

  fout = open(args.out_csv, 'w', newline='') if args.out_csv else sys.stdout
  writerow = csv.writer(fout).writerow
  writerow([
    'ver.SXF', 'Номенклатура', 'Масштаб', 'Название', 'Вид ИКМ', 'Тип ИКМ',
    'К.сумма'])
  for path in walk_args(args.dirs):
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
      sxf.kind_im, sxf.type_im, hex(sxf.crc))

if __name__ == '__main__':
  main()
