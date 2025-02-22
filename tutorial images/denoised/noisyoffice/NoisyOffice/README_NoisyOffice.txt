AIMS AND PURPOSES

This corpus is intended to do cleaning (or binarization) and enhancement of
noisy grayscale printed text images using supervised learning methods. To this
end, noisy images and their corresponding cleaned or binarized ground truth are
provided. Double resolution ground truth images are also provided in order to
test superresolution methods.

CORPUS DIRECTORIES STRUCTURE

SimulatedNoisyOffice folder has been prepared for training, validation and test
of supervised methods. RealNoisyOffice folder is provided for subjective
evaluation.

.
|-- RealNoisyOffice
|   |-- real_noisy_images_grayscale
|   `-- real_noisy_images_grayscale_doubleresolution
`-- SimulatedNoisyOffice
    |-- clean_images_binaryscale
    |-- clean_images_grayscale
    |-- clean_images_grayscale_doubleresolution
    `-- simulated_noisy_images_grayscale

RealNoisyOffice

- real_noisy_images_grayscale: 72 grayscale images of scanned "noisy" images.
- real_noisy_images_grayscale_doubleresolution: idem, double resolution.

SimulatedNoisyOffice

- simulated_noisy_images_grayscale: 72 grayscale images of scanned "simulated
  noisy" images for training, validation and test.
- clean_images_grayscale_doubleresolution: Grayscale ground truth of the images
  with double resolution.
- clean_images_grayscale: Grayscale ground truth of the images with smoothing on
  the borders (normal resolution).
- clean_images_binary: Binary ground truth of the images (normal resolution).

DESCRIPTION

Every file is a printed text image following the pattern FontABC_NoiseD_EE.png:

A) Size of the font: footnote size (f), normal size (n) o large size (L).

B) Font type: typewriter (t), sans serif (s) or roman (r). 

C) Yes/no emphasized font (e/m).

D) Type of noise: folded sheets (Noise f), wrinkled sheets (Noise w), coffee
   stains (Noise c), and footprints (Noise p).

E) Data set partition: training (TR), validation (VA), test (TE), real (RE).

For each type of font, one type of Noise: 17 files * 4 types of noise = 72
images.

OTHER INFORMATION

200 ppi => normal resolution
400 ppi => double resolution
