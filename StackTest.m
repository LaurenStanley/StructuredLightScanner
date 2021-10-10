%im = imread('C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\Stripes2.jpg');
im = imread('C:\Users\lesta\Downloads\m0sy7.png');
%imsum = sum(im, 3); % sum all channels
imsum=im;
h = fspecial('gaussian', 3);
disp(h)
im2 = imclose(imsum, ones(3)); % close
im2 = imfilter(im2, h); % smooth
imshow(im2)
% for each column, find regional max
%disp(size(im2))
mx = zeros(size(im2));
disp(size(mx))
for c = 1:size(im2, 2)
    mx(:, c) = imregionalmax(im2(:, c));
end
disp(mx)
% find connected components
%ccomp = bwlabel(mx);