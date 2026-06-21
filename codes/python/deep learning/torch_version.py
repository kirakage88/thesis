import torch
print(torch.cuda.is_available())  # Should print True
print(torch.version.cuda)          # Should print 13.0