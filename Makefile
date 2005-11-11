# Makefile for source rpm: imake
# $Id$
NAME := imake
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
