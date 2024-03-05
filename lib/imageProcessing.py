from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from time import time

class ImageHandler:
    def __init__(self, image: Image) -> None:
        """
        Used for processing images of the Sunspec project.

        Parameters
            image: PIL.Image
        """
        self.image = image
    
    def resize(self, size: list[int]) -> None:
        """
        Resizes the image stored in self.image using the PIL.Image.NEAREST method
        This method was chosen because of it's speed:accuracy

        Parameters
            size: list[int] = [int,int]
        """
        self.image.thumbnail(size, Image.NEAREST)
    
    def getPixelMaxs(self) -> np.ndarray:
        """
        Returns the MAX value of each pixel's RGB values

        Return
            np.ndarray
        """
        pixels: np.ndarray = np.array(self.image)
        maxs:   np.ndarray = np.amax(pixels, axis=2)
        return maxs
    
    def getHeatMapArray(self, size: list[int] = [16,9]) -> np.ndarray:
        """
        Calculates a heat map of MAX values from the image's RGB values

        Parameters
            size: list[int] = [int,int] ==> [16,9]
        
        Return
            np.ndarray
        """
        width:  int = size[0]
        height: int = size[1]
        data: np.ndarray = self.getPixelMaxs()
        section_width:  int = data.shape[1] // width
        section_height: int = data.shape[0] // height
        averages: list[np.floating] = []
        for height_index in range(height):
            for width_index in range(width):
                section: np.ndarray = data[height_index * section_height:(height_index + 1) * section_height, width_index * section_width:(width_index + 1) * section_width]
                average: np.floating = np.mean(section)
                averages.append(average)
        return np.array(averages).reshape(height, width)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        start = time()
        try:
            image = Image.open(sys.argv[1])
        except Exception:
            raise FileNotFoundError("The argument provided was invalid")
        img = ImageHandler(image)
        img.resize([640,360])
        img.image.save("new.jpg")
        heatmap_data = img.getHeatMapArray()
        max_index = np.unravel_index(np.argmax(heatmap_data), heatmap_data.shape)

        print(f"Took {time() - start} seconds")

        # Uncomment to see heatmap
        # plt.imshow(heatmap_data, cmap='hot', interpolation='nearest')
        # plt.colorbar()
        # plt.text(max_index[1], max_index[0], f"Max", color='black', fontsize=8, ha='center')
        # plt.show()
    else:
        raise ValueError("No argument provided for file path")