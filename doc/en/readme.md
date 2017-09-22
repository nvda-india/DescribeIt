# DescribeIt #

DescribeIt was written by Manshul Belani, and is GPL V2, as required by being an NVDA addon.

* [Source available on Github:](https://github.com/nvda-india/DescribeIt)

## Background

When accessing web pages, a user may come across images for which alternate text is not provided and screen reader reads nothing. However there are a lot of cognition APIs available which can provide description of images whose URL is provided to the API. This add on is written to use Microsoft cognition API for this function and provide the user with description of the image. 

## TLDR usage instructions

When navigating on a web page, if user comes across a graphic and presses NVDA+g, NVDA will provide a description of the image as received from the cognition API. NVDA+gg will provide one line description, confidence level, dominant foreground color and background color in a browseable message.
