import utility
import linedraw


lines = linedraw.sketch("images/amongus.png")
print(lines)
utility.copyToPositionsTxt(lines)
linedraw.visualize(lines)
# penpal.drawTxtFile()
