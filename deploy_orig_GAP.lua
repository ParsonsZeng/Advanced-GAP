require 'nn';
require 'image';
mnist = require 'mnist';
require 'optim';
require 'gnuplot';

model = torch.load('model_MNIST2.t7')

model:remove(13)
model:remove(12)
model:remove(11)
model:remove(10)
model:remove(9)
model:remove(8)
model:remove(7)

model2 = torch.load('gapWeights_MNIST2.t7')
weights = model2:get(1).weight

print('loading image')
img = image.load('imageNum.jpg',1)
img = img:double():reshape(1,img:size(1),img:size(2))

filters = model:forward(img)

for i=1,10 do
	local W = weights[i]
	local CAM = torch.Tensor(filters:size(2),filters:size(3))
	local CAM = W[1]*filters[1]
	for j=2,filters:size(1) do
		CAM = CAM + W[j]*(filters[j])
	end
	CAM:add(-CAM:min())
	CAM:div(CAM:max())
	CAM = image.scale(CAM,"*2")
	image.save('orig_GAP_results/imageNum_fil'..i..'.jpg',CAM)
	collectgarbage()
end