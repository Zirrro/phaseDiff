clc; clear all;
data = xlsread("C:\Users\shima\Desktop\程序\phaseDiff\diff.xlsx");
x = data(:,1);
y = data(:,2);
plot(x, y)