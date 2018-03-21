#!/bin/bash
for f in pos/*.jpg
do
        opencv_createsamples -img 'pos/*.jpg' -bg bg.txt -info info/info.lst -pngoutput info -maxxangle 0.1 -maxyangle 0.2 -maxzangle 0.2 -num 85
done


opencv_createsamples -img 'pos/1.jpg' -bg bg.txt -info info/info.lst -pngoutput info -maxxangle 0.1 -maxyangle 0.2 -maxzangle 0.2 -num 1800

opencv_createsamples -info info/info.lst -num 1800 -w 30 -h 30 -vec positives.vec

nohup opencv_traincascade -data data -vec positives.vec -bg bg.txt -numPos 1800 -numNeg 1000 -numStages 10 -w 30 -h 30

opencv_createsamples -img 'pos/30.jpg' -bg bg.txt -info info/info.lst -pngoutput info -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num 1950
