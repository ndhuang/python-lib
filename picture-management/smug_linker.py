'''
Notes on wordpress hero theme:

'''

BORDERSTYLE = "border:12px solid transparent;"

import argparse
import re

def parseHTML(html):
    '''
    Parse the smugmug link for the things we need.  The return is
    link, src, alt
    '''
    regex = '<a href="(\S+)"><img src="(\S+)".*alt="(.*)"></a>'
    match = re.match(regex, html)
    return match.groups()[:-1]

def rebuildHTML(link, src, alt, style, css_cls):
    '''
    Rebuild an html line that displays the image, and links back to something
    '''
    img = '<a href="{link!s}"><img class="{css_cls!s}" src="{src!s}" alt="{alt\
!s}" style="{style!s}"></a>'.format(link = link, src = src, alt = alt, style = style,css_cls = css_cls)
    return img

def replaceSize(src, new_size):
    '''
    Display an image of a different size
    '''
    regex = '\S+.smugmug.com/\S+/(\w+)/\S+-(\w+)\.jpg'
    match = re.match(regex, src)
    return new_size.join([src[:match.start(1)], src[match.end(1):match.start(2)], src[match.end(2):]])
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('html',
                         help = 'The embed link ("Gallery Link") from smugmug')
    parser.add_argument('--alt', '-a', type = str, default = '', 
                       help = 'The alt text for the image')
    parser.add_argument('--size', '-s', type = str, default = None,
                        choices = ['S', 's', 'M', 'm', 'L', 'l', 'XL', 'xl',
                                   'XS', 'xs', 'TH', 'th', 'X2', 'x2', 
                                   'X3', 'x3', 'O', 'o'],
                        help = 'The size of the image')
    parser.add_argument('--link', '-l', default = None,
                        help = 'The URL the image should link to.  If SAME, then link to the image source.  If not set, the link in the provided html is used.')
    parser.add_argument('--style', default = '',
                        help = 'The CSS style to apply')
    parser.add_argument('--class', default = '', dest = 'css_cls',
                        help = 'The CSS class to apply')
    parser.add_argument('--force-width', type = int, default = None,
                        help = 'Use the html width tag to set the image max-width')
    parser.add_argument('--border', action = 'store_true', 
                        help = "Add a nice border (border:12px solid transparent;)")
    args = parser.parse_args()
    link, src = parseHTML(args.html)
    if args.link is None:
        args.link = link
    elif args.link == 'SAME':
        raise NotImplementedError('fix it, bub')
        # the idea is to link to the original image- in full size
    if args.size is not None:
        src = replaceSize(src, args.size)
    if args.border:
        if args.style.endswith(';') or len(args.style) == 0:
            args.style += BORDERSTYLE
        else:
            args.style += ';' + BORDERSTYLE
    img = rebuildHTML(args.link, src, args.alt, args.style, args.css_cls)
    print '<figure>'
    print img
    if args.border:
        print '<figcaption style="{}"> </figcaption>'.format(args.style)
    else:
        print '<figcaption> </figcaption>'
    print '</figure>'
