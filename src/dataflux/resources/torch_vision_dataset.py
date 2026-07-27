from torchvision import datasets

TORCHVISION_DATASETS = {
    # MNIST Family
    "mnist": datasets.MNIST,
    "fashion_mnist": datasets.FashionMNIST,
    "kmnist": datasets.KMNIST,
    "emnist": datasets.EMNIST,
    "qmnist": datasets.QMNIST,
    "moving_mnist": datasets.MovingMNIST,

    # CIFAR
    "cifar10": datasets.CIFAR10,
    "cifar100": datasets.CIFAR100,

    # SVHN / USPS / SEMEION
    "svhn": datasets.SVHN,
    "usps": datasets.USPS,
    "semeion": datasets.SEMEION,

    # STL
    "stl10": datasets.STL10,

    # Image Classification
    "caltech101": datasets.Caltech101,
    "caltech256": datasets.Caltech256,
    "celeba": datasets.CelebA,
    "country211": datasets.Country211,
    "dtd": datasets.DTD,
    "eurosat": datasets.EuroSAT,
    "fer2013": datasets.FER2013,
    "fgvc_aircraft": datasets.FGVCAircraft,
    "flowers102": datasets.Flowers102,
    "food101": datasets.Food101,
    "gtsrb": datasets.GTSRB,
    "imagenette": datasets.Imagenette,
    "inaturalist": datasets.INaturalist,
    "imagenet": datasets.ImageNet,
    "lsun": datasets.LSUN,
    "omniglot": datasets.Omniglot,
    "oxford_iiit_pet": datasets.OxfordIIITPet,
    "pcam": datasets.PCAM,
    "places365": datasets.Places365,
    "rendered_sst2": datasets.RenderedSST2,
    "stanford_cars": datasets.StanfordCars,
    "sun397": datasets.SUN397,

    # Detection / Segmentation
    "cityscapes": datasets.Cityscapes,
    "coco_captions": datasets.CocoCaptions,
    "coco_detection": datasets.CocoDetection,
    "voc_detection": datasets.VOCDetection,
    "voc_segmentation": datasets.VOCSegmentation,
    "sbdataset": datasets.SBDataset,
    "widerface": datasets.WIDERFace,

    # Video
    "hmdb51": datasets.HMDB51,
    "kinetics": datasets.Kinetics,
    "ucf101": datasets.UCF101,

    # Stereo / Optical Flow
    "carla_stereo": datasets.CarlaStereo,
    "crestereo": datasets.CREStereo,
    "eth3d_stereo": datasets.ETH3DStereo,
    "fallingthings_stereo": datasets.FallingThingsStereo,
    "flyingchairs": datasets.FlyingChairs,
    "flyingthings3d": datasets.FlyingThings3D,
    "hd1k": datasets.HD1K,
    "instereo2k": datasets.InStereo2k,
    "kitti2012_stereo": datasets.Kitti2012Stereo,
    "kitti2015_stereo": datasets.Kitti2015Stereo,
    "kitti_flow": datasets.KittiFlow,
    "middlebury2014_stereo": datasets.Middlebury2014Stereo,
    "sceneflow_stereo": datasets.SceneFlowStereo,
    "sintel": datasets.Sintel,
    "sintel_stereo": datasets.SintelStereo,

    # Miscellaneous
    "clevr_classification": datasets.CLEVRClassification,
    "fake_data": datasets.FakeData,
    "flickr8k": datasets.Flickr8k,
    "flickr30k": datasets.Flickr30k,
    "kitti": datasets.Kitti,
    "lfw_people": datasets.LFWPeople,
    "lfw_pairs": datasets.LFWPairs,
    "phototour": datasets.PhotoTour,
    "sbu": datasets.SBU,
}