data=readtable('demo1.csv');

x1=data.pt1x;   
y1=data.pt1y;
z1=data.pt1z;
x2=data.pt2x;
y2=data.pt2y;
z2=data.pt2z;

colormap(jet);
colorbar;
h1 = scatter3(x1, y1, z1,30,z1, 'filled');
axis equal;
hold on;
h2 = scatter3(x2, y2, z2,30,z2, 'filled');
xlabel('X');
ylabel('Y');
zlabel('Z');
title('3D Point Animation from Blue to White');
grid on;
% count=numel(x1);
% animationTime = 20; 
% j = 1; 

frames=5000;
for t=1:frames
    color_shift = sin(2 * pi * t / frames);
    c = (y1 - min(y1)) / (max(y1) - min(y1));
    c = c + color_shift;
    c = mod(c, 1);
    h1.CData = c;
    h2.CData = c;
    pause(0.0005);
end

