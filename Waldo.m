waldo = imread('Waldo.png');

%waldo = imread('TheGobblingGluttons.jpg');
%waldo = imread('DepartmentStore.jpg');

figure(1)
clf
image(waldo);
axis equal
axis tight

%Our goal is to build a filter that finds Waldo.  This will be done by
%analyzing a component of the image containing Waldo-like features.
%
%Since Waldo's stripes are red and white, how do we combine the r,g, and b
%images to make a grayscale image where the stripes are black and white?
%
%Our transformation will be: red - (.5*green + .5*blue)

waldo2D = double(waldo(:,:,1)-.5*waldo(:,:,2)-.5*waldo(:,:,3));
waldo2D = waldo2D-mean(waldo2D(:));

figure(1)
clf
imagesc(waldo2D)
colormap(gray);
axis equal
axis tight

%Let the user click on a possible location of 'Waldo' (e.g. stripes) and crop the
%image down to the region around where the mouse was clicked. Then show the
%cropped image in figure 2.
%
%The user input is done with 'ginput' which waits for the user to click the
%mouse on the current figure and returns the x and y positions.  the '1'
%means wait for just one click.

figure(1)
[xClick,yClick] = ginput(1);
xClick = round(xClick);
yClick = round(yClick);

%size of square patch (pixels)
sz = 50;

patch2D  = waldo2D(yClick-sz/2:yClick+sz/2-1,xClick-sz/2:xClick+sz/2-1);

[xx,yy] = meshgrid(linspace(-sz/2,sz/2,sz));
patch2D= patch2D-mean(patch2D(:));

figure(2)
clf
plotFFT2(patch2D);

subplot(1,2,1);
[foo,sf] = ginput(1);
disp(sf)

disp(sprintf('Spatial Frequency: %5.2f cycles/pixel',sf));

sigma = 1/sf;  %width of Gaussian (1/e half-width)
Gaussian = exp(-(xx.^2+yy.^2)/sigma^2);

gratingSin = sin(2*pi*sf*yy);
GaborSin = gratingSin.*Gaussian;
figure(2)
clf
plotFFT2(GaborSin);

filtImgSin = conv2(waldo2D,GaborSin,'same');

figure(3)
clf
imagesc(filtImgSin);
axis equal
axis off
colormap(gray);

gratingCos = cos(2*pi*sf*yy);
GaborCos = gratingCos.*Gaussian;

filtImgCos = conv2(waldo2D,GaborCos,'same');

filtImg = sqrt(filtImgSin.^2+filtImgCos.^2);

figure(3)
clf
imagesc(filtImg)
axis equal
axis off
colormap(gray);

attenuateImg = filtImg/max(filtImg(:));
attenuateImg = (attenuateImg+.25)/1.25;

newImg = uint8(double(waldo).*repmat(attenuateImg,[1,1,3]));
figure(3)
clf

image(newImg);
axis equal
axis off