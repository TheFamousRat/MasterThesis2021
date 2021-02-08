{
    "header": {
        "pipelineVersion": "2.2",
        "releaseVersion": "2020.1.0",
        "fileVersion": "1.1",
        "nodesVersions": {
            "Meshing": "6.0",
            "FeatureExtraction": "1.1",
            "ImageMatching": "2.0",
            "PrepareDenseScene": "3.0",
            "MeshFiltering": "2.0",
            "FeatureMatching": "2.0",
            "CameraInit": "3.0",
            "Texturing": "5.0",
            "StructureFromMotion": "2.0",
            "DepthMapFilter": "3.0",
            "DepthMap": "2.0"
        }
    },
    "graph": {
        "CameraInit_1": {
            "nodeType": "CameraInit",
            "position": [
                0,
                0
            ],
            "parallelization": {
                "blockSize": 0,
                "size": 80,
                "split": 1
            },
            "uids": {
                "0": "5ad5c5c7fce241fdd48a1398c1d4511ff394d3cc"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "viewpoints": [
                    {
                        "viewId": 19072020,
                        "poseId": 19072020,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151126.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:26\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:26\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:26\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"72\", \"Exif:SubsecTimeDigitized\": \"72\", \"Exif:SubsecTimeOriginal\": \"72\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"125\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 80425919,
                        "poseId": 80425919,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151234.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:34\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:34\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:34\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"165\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"24\", \"Exif:SubsecTimeDigitized\": \"24\", \"Exif:SubsecTimeOriginal\": \"24\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"36\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 84007612,
                        "poseId": 84007612,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151115.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:15\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:15\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:15\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"57\", \"Exif:SubsecTimeDigitized\": \"57\", \"Exif:SubsecTimeOriginal\": \"57\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"126\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 86162162,
                        "poseId": 86162162,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151041.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:41\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:41\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:41\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"75\", \"Exif:SubsecTimeDigitized\": \"75\", \"Exif:SubsecTimeOriginal\": \"75\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"128\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 105656540,
                        "poseId": 105656540,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151232.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:32\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:32\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:32\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"184\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"70\", \"Exif:SubsecTimeDigitized\": \"70\", \"Exif:SubsecTimeOriginal\": \"70\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"31\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 143512853,
                        "poseId": 143512853,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151031.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:31\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:31\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:31\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"33\", \"Exif:SubsecTimeDigitized\": \"33\", \"Exif:SubsecTimeOriginal\": \"33\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"128\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 143958042,
                        "poseId": 143958042,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151034.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:34\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:34\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:34\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"67\", \"Exif:SubsecTimeDigitized\": \"67\", \"Exif:SubsecTimeOriginal\": \"67\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"132\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 217786876,
                        "poseId": 217786876,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151149.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:49\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:49\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:49\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"201\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"71\", \"Exif:SubsecTimeDigitized\": \"71\", \"Exif:SubsecTimeOriginal\": \"71\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"128\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 250898890,
                        "poseId": 250898890,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151249.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:49\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:49\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:49\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"203\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"61\", \"Exif:SubsecTimeDigitized\": \"61\", \"Exif:SubsecTimeOriginal\": \"61\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"39\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 258915278,
                        "poseId": 258915278,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151210.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:10\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:10\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:10\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"159\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"33\", \"Exif:SubsecTimeDigitized\": \"33\", \"Exif:SubsecTimeOriginal\": \"33\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"30\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 318685589,
                        "poseId": 318685589,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151016.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:17\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:17\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:17\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"204\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"43\", \"Exif:SubsecTimeDigitized\": \"43\", \"Exif:SubsecTimeOriginal\": \"43\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"134\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 358312878,
                        "poseId": 358312878,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151218.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:18\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:18\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:18\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"142\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"16\", \"Exif:SubsecTimeDigitized\": \"16\", \"Exif:SubsecTimeOriginal\": \"16\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"25\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 369219788,
                        "poseId": 369219788,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151046.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:46\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:46\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:46\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"82\", \"Exif:SubsecTimeDigitized\": \"82\", \"Exif:SubsecTimeOriginal\": \"82\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"128\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 416397099,
                        "poseId": 416397099,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151122.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:22\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:22\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:22\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"78\", \"Exif:SubsecTimeDigitized\": \"78\", \"Exif:SubsecTimeOriginal\": \"78\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"124\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 489799943,
                        "poseId": 489799943,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151235.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:35\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:35\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:35\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"165\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"70\", \"Exif:SubsecTimeDigitized\": \"70\", \"Exif:SubsecTimeOriginal\": \"70\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"28\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 527887742,
                        "poseId": 527887742,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151148.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:48\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:48\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:48\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"201\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"14\", \"Exif:SubsecTimeDigitized\": \"14\", \"Exif:SubsecTimeOriginal\": \"14\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"127\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 529549594,
                        "poseId": 529549594,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151253.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:53\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:53\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:53\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"203\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"99\", \"Exif:SubsecTimeDigitized\": \"99\", \"Exif:SubsecTimeOriginal\": \"99\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"35\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 589943636,
                        "poseId": 589943636,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151152.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:52\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:52\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:52\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"201\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"73\", \"Exif:SubsecTimeDigitized\": \"73\", \"Exif:SubsecTimeOriginal\": \"73\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"129\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 591307001,
                        "poseId": 591307001,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151239.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:40\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:40\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:40\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"141\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"44\", \"Exif:SubsecTimeDigitized\": \"44\", \"Exif:SubsecTimeOriginal\": \"44\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"31\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 648061514,
                        "poseId": 648061514,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151052.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:52\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:52\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:52\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"69\", \"Exif:SubsecTimeDigitized\": \"69\", \"Exif:SubsecTimeOriginal\": \"69\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"130\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 650901653,
                        "poseId": 650901653,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151102.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:02\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:02\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:02\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"68\", \"Exif:SubsecTimeDigitized\": \"68\", \"Exif:SubsecTimeOriginal\": \"68\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"130\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 668346660,
                        "poseId": 668346660,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151222.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:22\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:22\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:22\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"142\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"13\", \"Exif:SubsecTimeDigitized\": \"13\", \"Exif:SubsecTimeOriginal\": \"13\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"28\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 700871086,
                        "poseId": 700871086,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151112.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:12\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:12\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:12\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"32\", \"Exif:SubsecTimeDigitized\": \"32\", \"Exif:SubsecTimeOriginal\": \"32\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"127\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 756694745,
                        "poseId": 756694745,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151027.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:27\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:27\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:27\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"95\", \"Exif:SubsecTimeDigitized\": \"95\", \"Exif:SubsecTimeOriginal\": \"95\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"129\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 759109756,
                        "poseId": 759109756,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151246.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:46\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:46\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:46\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"203\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"78\", \"Exif:SubsecTimeDigitized\": \"78\", \"Exif:SubsecTimeOriginal\": \"78\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"34\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 769906964,
                        "poseId": 769906964,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151045.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:45\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:45\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:45\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"34\", \"Exif:SubsecTimeDigitized\": \"34\", \"Exif:SubsecTimeOriginal\": \"34\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"126\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 774310894,
                        "poseId": 774310894,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151245.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:45\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:45\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:45\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"203\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"16\", \"Exif:SubsecTimeDigitized\": \"16\", \"Exif:SubsecTimeOriginal\": \"16\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"39\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 820651174,
                        "poseId": 820651174,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151243.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:43\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:43\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:43\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"203\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"83\", \"Exif:SubsecTimeDigitized\": \"83\", \"Exif:SubsecTimeOriginal\": \"83\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"35\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 858016180,
                        "poseId": 858016180,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151256.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:56\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:56\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:56\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"203\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"84\", \"Exif:SubsecTimeDigitized\": \"84\", \"Exif:SubsecTimeOriginal\": \"84\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"41\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 892150344,
                        "poseId": 892150344,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151211.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:11\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:11\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:11\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"159\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"60\", \"Exif:SubsecTimeDigitized\": \"60\", \"Exif:SubsecTimeOriginal\": \"60\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"28\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 907512580,
                        "poseId": 907512580,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151029.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:29\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:29\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:29\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"71\", \"Exif:SubsecTimeDigitized\": \"71\", \"Exif:SubsecTimeOriginal\": \"71\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"127\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 958666789,
                        "poseId": 958666789,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151252.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:52\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:52\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:52\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"203\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"76\", \"Exif:SubsecTimeDigitized\": \"76\", \"Exif:SubsecTimeOriginal\": \"76\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"35\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 962906967,
                        "poseId": 962906967,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151155.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:55\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:55\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:55\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"201\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"85\", \"Exif:SubsecTimeDigitized\": \"85\", \"Exif:SubsecTimeOriginal\": \"85\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"133\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1028499848,
                        "poseId": 1028499848,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151216.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:16\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:16\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:16\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"142\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"88\", \"Exif:SubsecTimeDigitized\": \"88\", \"Exif:SubsecTimeOriginal\": \"88\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"30\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1037019384,
                        "poseId": 1037019384,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151220.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:20\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:20\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:20\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"142\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"79\", \"Exif:SubsecTimeDigitized\": \"79\", \"Exif:SubsecTimeOriginal\": \"79\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"30\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1047315610,
                        "poseId": 1047315610,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151157.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:57\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:57\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:57\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"201\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"53\", \"Exif:SubsecTimeDigitized\": \"53\", \"Exif:SubsecTimeOriginal\": \"53\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"131\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1068528069,
                        "poseId": 1068528069,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151146.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:46\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:46\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:46\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"201\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"47\", \"Exif:SubsecTimeDigitized\": \"47\", \"Exif:SubsecTimeOriginal\": \"47\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"130\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1088568702,
                        "poseId": 1088568702,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151144.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:44\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:44\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:44\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"201\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"80\", \"Exif:SubsecTimeDigitized\": \"80\", \"Exif:SubsecTimeOriginal\": \"80\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"131\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1110953291,
                        "poseId": 1110953291,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151116.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:16\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:16\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:16\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"91\", \"Exif:SubsecTimeDigitized\": \"91\", \"Exif:SubsecTimeOriginal\": \"91\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"128\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1119862382,
                        "poseId": 1119862382,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151258.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:58\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:58\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:58\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"203\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"25\", \"Exif:SubsecTimeDigitized\": \"25\", \"Exif:SubsecTimeOriginal\": \"25\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"29\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1126454843,
                        "poseId": 1126454843,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151212.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:12\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:12\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:12\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"159\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"86\", \"Exif:SubsecTimeDigitized\": \"86\", \"Exif:SubsecTimeOriginal\": \"86\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"33\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1136794381,
                        "poseId": 1136794381,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151238.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:38\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:38\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:38\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"165\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"47\", \"Exif:SubsecTimeDigitized\": \"47\", \"Exif:SubsecTimeOriginal\": \"47\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"42\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1141313858,
                        "poseId": 1141313858,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151128.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:28\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:28\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:28\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"55\", \"Exif:SubsecTimeDigitized\": \"55\", \"Exif:SubsecTimeOriginal\": \"55\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"126\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1141759952,
                        "poseId": 1141759952,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151108.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:08\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:08\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:08\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"78\", \"Exif:SubsecTimeDigitized\": \"78\", \"Exif:SubsecTimeOriginal\": \"78\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"131\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1155511619,
                        "poseId": 1155511619,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151228.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:28\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:28\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:28\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"184\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"27\", \"Exif:SubsecTimeDigitized\": \"27\", \"Exif:SubsecTimeOriginal\": \"27\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"37\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1158557467,
                        "poseId": 1158557467,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151113.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:13\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:13\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:13\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"82\", \"Exif:SubsecTimeDigitized\": \"82\", \"Exif:SubsecTimeOriginal\": \"82\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"128\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1178224298,
                        "poseId": 1178224298,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151104.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:04\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:04\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:04\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"95\", \"Exif:SubsecTimeDigitized\": \"95\", \"Exif:SubsecTimeOriginal\": \"95\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"128\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1191594298,
                        "poseId": 1191594298,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151151.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:51\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:51\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:51\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"201\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"33\", \"Exif:SubsecTimeDigitized\": \"33\", \"Exif:SubsecTimeOriginal\": \"33\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"129\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1215711816,
                        "poseId": 1215711816,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151026.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:26\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:26\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:26\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"23\", \"Exif:SubsecTimeDigitized\": \"23\", \"Exif:SubsecTimeOriginal\": \"23\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"130\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1230339997,
                        "poseId": 1230339997,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151035.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:36\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:36\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:36\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"99\", \"Exif:SubsecTimeDigitized\": \"99\", \"Exif:SubsecTimeOriginal\": \"99\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"129\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1256712154,
                        "poseId": 1256712154,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151018.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:19\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:19\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:19\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"204\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"51\", \"Exif:SubsecTimeDigitized\": \"51\", \"Exif:SubsecTimeOriginal\": \"51\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"129\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1309637185,
                        "poseId": 1309637185,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151250.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:51\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:51\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:51\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"203\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"13\", \"Exif:SubsecTimeDigitized\": \"13\", \"Exif:SubsecTimeOriginal\": \"13\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"40\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1333044175,
                        "poseId": 1333044175,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151032.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:32\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:32\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:32\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"96\", \"Exif:SubsecTimeDigitized\": \"96\", \"Exif:SubsecTimeOriginal\": \"96\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"133\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1375157905,
                        "poseId": 1375157905,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151141.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:41\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:41\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:41\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"201\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"99\", \"Exif:SubsecTimeDigitized\": \"99\", \"Exif:SubsecTimeOriginal\": \"99\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"134\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1391585163,
                        "poseId": 1391585163,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151259.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:59\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:59\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:59\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"203\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"56\", \"Exif:SubsecTimeDigitized\": \"56\", \"Exif:SubsecTimeOriginal\": \"56\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"38\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1411374049,
                        "poseId": 1411374049,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151024.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:24\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:24\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:24\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"164\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"40\", \"Exif:SubsecTimeDigitized\": \"40\", \"Exif:SubsecTimeOriginal\": \"40\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"130\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1423586691,
                        "poseId": 1423586691,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151110.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:10\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:10\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:10\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"25\", \"Exif:SubsecTimeDigitized\": \"25\", \"Exif:SubsecTimeOriginal\": \"25\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"129\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1465221751,
                        "poseId": 1465221751,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151059.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:59\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:59\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:59\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"19\", \"Exif:SubsecTimeDigitized\": \"19\", \"Exif:SubsecTimeOriginal\": \"19\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"128\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1480714339,
                        "poseId": 1480714339,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151248.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:48\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:48\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:48\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"203\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"27\", \"Exif:SubsecTimeDigitized\": \"27\", \"Exif:SubsecTimeOriginal\": \"27\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"37\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1483655858,
                        "poseId": 1483655858,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151056.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:56\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:56\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:56\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"30\", \"Exif:SubsecTimeDigitized\": \"30\", \"Exif:SubsecTimeOriginal\": \"30\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"131\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1527533204,
                        "poseId": 1527533204,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151214.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:14\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:14\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:14\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"142\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"16\", \"Exif:SubsecTimeDigitized\": \"16\", \"Exif:SubsecTimeOriginal\": \"16\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"26\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1555114700,
                        "poseId": 1555114700,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151231.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:31\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:31\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:31\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"184\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"23\", \"Exif:SubsecTimeDigitized\": \"23\", \"Exif:SubsecTimeOriginal\": \"23\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"36\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1603936302,
                        "poseId": 1603936302,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151255.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:55\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:55\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:55\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"203\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"35\", \"Exif:SubsecTimeDigitized\": \"35\", \"Exif:SubsecTimeOriginal\": \"35\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"37\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1615403711,
                        "poseId": 1615403711,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151135.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:35\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:35\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:35\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"175\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"42\", \"Exif:SubsecTimeDigitized\": \"42\", \"Exif:SubsecTimeOriginal\": \"42\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"134\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1645328277,
                        "poseId": 1645328277,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151057.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:57\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:57\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:57\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"74\", \"Exif:SubsecTimeDigitized\": \"74\", \"Exif:SubsecTimeOriginal\": \"74\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"129\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1713724881,
                        "poseId": 1713724881,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151100.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:00\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:00\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:00\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"83\", \"Exif:SubsecTimeDigitized\": \"83\", \"Exif:SubsecTimeOriginal\": \"83\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"131\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1730339861,
                        "poseId": 1730339861,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151223.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:23\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:23\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:23\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"126\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"49\", \"Exif:SubsecTimeDigitized\": \"49\", \"Exif:SubsecTimeOriginal\": \"49\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.020003\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"33\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1732588663,
                        "poseId": 1732588663,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151038.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:38\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:38\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:38\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"85\", \"Exif:SubsecTimeDigitized\": \"85\", \"Exif:SubsecTimeOriginal\": \"85\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"130\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1745779698,
                        "poseId": 1745779698,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151037.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:37\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:37\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:37\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"48\", \"Exif:SubsecTimeDigitized\": \"48\", \"Exif:SubsecTimeOriginal\": \"48\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"127\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1768603455,
                        "poseId": 1768603455,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151236.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:37\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:37\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:37\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"165\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"87\", \"Exif:SubsecTimeDigitized\": \"87\", \"Exif:SubsecTimeOriginal\": \"87\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"37\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1770069921,
                        "poseId": 1770069921,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151015.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:15\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:15\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:15\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"204\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"70\", \"Exif:SubsecTimeDigitized\": \"70\", \"Exif:SubsecTimeOriginal\": \"70\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"130\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1800559957,
                        "poseId": 1800559957,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151124.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:24\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:24\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:24\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"71\", \"Exif:SubsecTimeDigitized\": \"71\", \"Exif:SubsecTimeOriginal\": \"71\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"126\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1809225894,
                        "poseId": 1809225894,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151159.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:59\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:59\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:59\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"201\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"37\", \"Exif:SubsecTimeDigitized\": \"37\", \"Exif:SubsecTimeOriginal\": \"37\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"130\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1867180194,
                        "poseId": 1867180194,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151106.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:06\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:06\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:06\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"25\", \"Exif:SubsecTimeDigitized\": \"25\", \"Exif:SubsecTimeOriginal\": \"25\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"132\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1924377308,
                        "poseId": 1924377308,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151219.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:19\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:19\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:19\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"142\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"40\", \"Exif:SubsecTimeDigitized\": \"40\", \"Exif:SubsecTimeOriginal\": \"40\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"26\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1992305963,
                        "poseId": 1992305963,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151215.jpg",
                        "intrinsicId": 2402326443,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:12:15\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:12:15\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:12:15\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"142\", \"Exif:PixelXDimension\": \"4192\", \"Exif:PixelYDimension\": \"3104\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"46\", \"Exif:SubsecTimeDigitized\": \"46\", \"Exif:SubsecTimeOriginal\": \"46\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.029999\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"25\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2094281695,
                        "poseId": 2094281695,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151118.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:18\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:18\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:18\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"38\", \"Exif:SubsecTimeDigitized\": \"38\", \"Exif:SubsecTimeOriginal\": \"38\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"126\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2111849580,
                        "poseId": 2111849580,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151107.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:07\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:07\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:07\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"61\", \"Exif:SubsecTimeDigitized\": \"61\", \"Exif:SubsecTimeOriginal\": \"61\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"128\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2137384340,
                        "poseId": 2137384340,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151043.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:10:43\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:10:43\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:10:43\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"181\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"58\", \"Exif:SubsecTimeDigitized\": \"58\", \"Exif:SubsecTimeOriginal\": \"58\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"129\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2141025181,
                        "poseId": 2141025181,
                        "path": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset/P81019-151139.jpg",
                        "intrinsicId": 2905769803,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"AliceVision:SensorWidth\": \"4.690000\", \"DateTime\": \"2018:10:19 15:11:40\", \"Exif:ColorSpace\": \"1\", \"Exif:DateTimeDigitized\": \"2018:10:19 15:11:40\", \"Exif:DateTimeOriginal\": \"2018:10:19 15:11:40\", \"Exif:DigitalZoomRatio\": \"1\", \"Exif:ExifVersion\": \"0220\", \"Exif:ExposureBiasValue\": \"0\", \"Exif:ExposureMode\": \"0\", \"Exif:ExposureProgram\": \"0\", \"Exif:Flash\": \"0\", \"Exif:FlashPixVersion\": \"0100\", \"Exif:FocalLength\": \"3.81\", \"Exif:LightSource\": \"255\", \"Exif:MeteringMode\": \"2\", \"Exif:PhotographicSensitivity\": \"187\", \"Exif:PixelXDimension\": \"3104\", \"Exif:PixelYDimension\": \"4192\", \"Exif:SceneCaptureType\": \"0\", \"Exif:SubsecTime\": \"46\", \"Exif:SubsecTimeDigitized\": \"46\", \"Exif:SubsecTimeOriginal\": \"46\", \"Exif:WhiteBalance\": \"0\", \"Exif:YCbCrPositioning\": \"2\", \"ExposureTime\": \"0.009996\", \"FNumber\": \"2.2\", \"GPS:ImgDirection\": \"125\", \"GPS:ImgDirectionRef\": \"M\", \"ImageDescription\": \"\", \"Make\": \"Meizu\", \"Model\": \"m1 note\", \"Orientation\": \"1\", \"ResolutionUnit\": \"none\", \"Software\": \"MediaTek Camera Application\\n\", \"XResolution\": \"72\", \"YResolution\": \"72\", \"jpeg:subsampling\": \"4:2:2\", \"oiio:ColorSpace\": \"sRGB\"}"
                    }
                ],
                "intrinsics": [
                    {
                        "intrinsicId": 2402326443,
                        "pxInitialFocalLength": 3405.4413646055436,
                        "pxFocalLength": 3405.4413646055436,
                        "type": "radial3",
                        "width": 4192,
                        "height": 3104,
                        "sensorWidth": 4.69,
                        "sensorHeight": 3.4727480916030533,
                        "serialNumber": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset_Meizu_m1 note",
                        "principalPoint": {
                            "x": 2096.0,
                            "y": 1552.0
                        },
                        "initializationMode": "estimated",
                        "distortionParams": [
                            0.0,
                            0.0,
                            0.0
                        ],
                        "locked": false
                    },
                    {
                        "intrinsicId": 2905769803,
                        "pxInitialFocalLength": 3405.4413646055436,
                        "pxFocalLength": 3405.4413646055436,
                        "type": "radial3",
                        "width": 3104,
                        "height": 4192,
                        "sensorWidth": 4.69,
                        "sensorHeight": 3.4727480916030538,
                        "serialNumber": "/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/dataset_flowerpot/full_dataset_Meizu_m1 note",
                        "principalPoint": {
                            "x": 1552.0,
                            "y": 2096.0
                        },
                        "initializationMode": "estimated",
                        "distortionParams": [
                            0.0,
                            0.0,
                            0.0
                        ],
                        "locked": false
                    }
                ],
                "sensorDatabase": "/home/thefamousrat/Downloads/Meshroom-2020.1.0/aliceVision/share/aliceVision/cameraSensors.db",
                "defaultFieldOfView": 45.0,
                "groupCameraFallback": "folder",
                "allowedCameraModels": [
                    "pinhole",
                    "radial1",
                    "radial3",
                    "brown",
                    "fisheye4",
                    "fisheye1"
                ],
                "viewIdMethod": "metadata",
                "viewIdRegex": ".*?(\\d+)",
                "verboseLevel": "info"
            },
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/cameraInit.sfm"
            }
        },
        "FeatureExtraction_1": {
            "nodeType": "FeatureExtraction",
            "position": [
                155,
                0
            ],
            "parallelization": {
                "blockSize": 40,
                "size": 80,
                "split": 2
            },
            "uids": {
                "0": "d5e7a3738010d992cb9a0026266c917fc4da319a"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "input": "{CameraInit_1.output}",
                "describerTypes": [
                    "sift"
                ],
                "describerPreset": "normal",
                "forceCpuExtraction": true,
                "maxThreads": 0,
                "verboseLevel": "info"
            },
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/"
            }
        },
        "ImageMatching_1": {
            "nodeType": "ImageMatching",
            "position": [
                310,
                0
            ],
            "parallelization": {
                "blockSize": 0,
                "size": 80,
                "split": 1
            },
            "uids": {
                "0": "5aa3e022e3c9f21d8e6c642729c64740ecef253e"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "input": "{FeatureExtraction_1.input}",
                "featuresFolders": [
                    "{FeatureExtraction_1.output}"
                ],
                "method": "VocabularyTree",
                "tree": "/home/thefamousrat/Downloads/Meshroom-2020.1.0/aliceVision/share/aliceVision/vlfeat_K80L3.SIFT.tree",
                "weights": "",
                "minNbImages": 200,
                "maxDescriptors": 500,
                "nbMatches": 50,
                "nbNeighbors": 50,
                "verboseLevel": "info"
            },
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/imageMatches.txt"
            }
        },
        "FeatureMatching_1": {
            "nodeType": "FeatureMatching",
            "position": [
                465,
                0
            ],
            "parallelization": {
                "blockSize": 20,
                "size": 80,
                "split": 4
            },
            "uids": {
                "0": "bae66a9f9c6eee0ab348bd422b1a42d9d58435b6"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "input": "{ImageMatching_1.input}",
                "featuresFolders": "{ImageMatching_1.featuresFolders}",
                "imagePairsList": "{ImageMatching_1.output}",
                "describerTypes": [
                    "sift"
                ],
                "photometricMatchingMethod": "ANN_L2",
                "geometricEstimator": "acransac",
                "geometricFilterType": "fundamental_matrix",
                "distanceRatio": 0.8,
                "maxIteration": 2048,
                "geometricError": 0.0,
                "knownPosesGeometricErrorMax": 5.0,
                "maxMatches": 0,
                "savePutativeMatches": false,
                "guidedMatching": false,
                "matchFromKnownCameraPoses": false,
                "exportDebugFiles": false,
                "verboseLevel": "info"
            },
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/"
            }
        },
        "StructureFromMotion_1": {
            "nodeType": "StructureFromMotion",
            "position": [
                620,
                0
            ],
            "parallelization": {
                "blockSize": 0,
                "size": 80,
                "split": 1
            },
            "uids": {
                "0": "4e7daaf65d2168b45652ecb431979d4f4ec17868"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "input": "{FeatureMatching_1.input}",
                "featuresFolders": "{FeatureMatching_1.featuresFolders}",
                "matchesFolders": [
                    "{FeatureMatching_1.output}"
                ],
                "describerTypes": [
                    "sift"
                ],
                "localizerEstimator": "acransac",
                "observationConstraint": "Basic",
                "localizerEstimatorMaxIterations": 4096,
                "localizerEstimatorError": 0.0,
                "lockScenePreviouslyReconstructed": false,
                "useLocalBA": true,
                "localBAGraphDistance": 1,
                "maxNumberOfMatches": 0,
                "minNumberOfMatches": 0,
                "minInputTrackLength": 2,
                "minNumberOfObservationsForTriangulation": 2,
                "minAngleForTriangulation": 3.0,
                "minAngleForLandmark": 2.0,
                "maxReprojectionError": 4.0,
                "minAngleInitialPair": 5.0,
                "maxAngleInitialPair": 40.0,
                "useOnlyMatchesFromInputFolder": false,
                "useRigConstraint": true,
                "lockAllIntrinsics": false,
                "filterTrackForks": false,
                "initialPairA": "",
                "initialPairB": "",
                "interFileExtension": ".abc",
                "verboseLevel": "info"
            },
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/sfm.abc",
                "outputViewsAndPoses": "{cache}/{nodeType}/{uid0}/cameras.sfm",
                "extraInfoFolder": "{cache}/{nodeType}/{uid0}/"
            }
        },
        "PrepareDenseScene_1": {
            "nodeType": "PrepareDenseScene",
            "position": [
                775,
                0
            ],
            "parallelization": {
                "blockSize": 40,
                "size": 80,
                "split": 2
            },
            "uids": {
                "0": "f4bc049f95c8e0e76d57a5b1ad2f504703a56968"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "input": "{StructureFromMotion_1.output}",
                "imagesFolders": [],
                "outputFileType": "exr",
                "saveMetadata": true,
                "saveMatricesTxtFiles": false,
                "evCorrection": false,
                "verboseLevel": "info"
            },
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/",
                "outputUndistorted": "{cache}/{nodeType}/{uid0}/*.{outputFileTypeValue}"
            }
        },
        "DepthMap_1": {
            "nodeType": "DepthMap",
            "position": [
                930,
                0
            ],
            "parallelization": {
                "blockSize": 3,
                "size": 80,
                "split": 27
            },
            "uids": {
                "0": "5656b2355d3396084967311eca74c42e243d70de"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "input": "{PrepareDenseScene_1.input}",
                "imagesFolder": "{PrepareDenseScene_1.output}",
                "downscale": 2,
                "minViewAngle": 2.0,
                "maxViewAngle": 70.0,
                "sgmMaxTCams": 10,
                "sgmWSH": 4,
                "sgmGammaC": 5.5,
                "sgmGammaP": 8.0,
                "refineMaxTCams": 6,
                "refineNSamplesHalf": 150,
                "refineNDepthsToRefine": 31,
                "refineNiters": 100,
                "refineWSH": 3,
                "refineSigma": 15,
                "refineGammaC": 15.5,
                "refineGammaP": 8.0,
                "refineUseTcOrRcPixSize": false,
                "exportIntermediateResults": false,
                "nbGPUs": 0,
                "verboseLevel": "info"
            },
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/"
            }
        },
        "DepthMapFilter_1": {
            "nodeType": "DepthMapFilter",
            "position": [
                1085,
                0
            ],
            "parallelization": {
                "blockSize": 10,
                "size": 80,
                "split": 8
            },
            "uids": {
                "0": "b16950353af05e6ab749b37317b82ba389f3024b"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "input": "{DepthMap_1.input}",
                "depthMapsFolder": "{DepthMap_1.output}",
                "minViewAngle": 2.0,
                "maxViewAngle": 70.0,
                "nNearestCams": 10,
                "minNumOfConsistentCams": 3,
                "minNumOfConsistentCamsWithLowSimilarity": 4,
                "pixSizeBall": 0,
                "pixSizeBallWithLowSimilarity": 0,
                "computeNormalMaps": false,
                "verboseLevel": "info"
            },
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/"
            }
        },
        "Meshing_1": {
            "nodeType": "Meshing",
            "position": [
                1240,
                0
            ],
            "parallelization": {
                "blockSize": 0,
                "size": 1,
                "split": 1
            },
            "uids": {
                "0": "4d614643cfd542efd5165635752f285dba3449c5"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "input": "{DepthMapFilter_1.input}",
                "depthMapsFolder": "{DepthMapFilter_1.output}",
                "useBoundingBox": false,
                "boundingBox": {
                    "bboxTranslation": {
                        "x": 0.0,
                        "y": 0.0,
                        "z": 0.0
                    },
                    "bboxRotation": {
                        "x": 0.0,
                        "y": 0.0,
                        "z": 0.0
                    },
                    "bboxScale": {
                        "x": 1.0,
                        "y": 1.0,
                        "z": 1.0
                    }
                },
                "estimateSpaceFromSfM": true,
                "estimateSpaceMinObservations": 3,
                "estimateSpaceMinObservationAngle": 10,
                "maxInputPoints": 50000000,
                "maxPoints": 5000000,
                "maxPointsPerVoxel": 1000000,
                "minStep": 2,
                "partitioning": "singleBlock",
                "repartition": "multiResolution",
                "angleFactor": 15.0,
                "simFactor": 15.0,
                "pixSizeMarginInitCoef": 2.0,
                "pixSizeMarginFinalCoef": 4.0,
                "voteMarginFactor": 4.0,
                "contributeMarginFactor": 2.0,
                "simGaussianSizeInit": 10.0,
                "simGaussianSize": 10.0,
                "minAngleThreshold": 1.0,
                "refineFuse": true,
                "addLandmarksToTheDensePointCloud": false,
                "colorizeOutput": false,
                "saveRawDensePointCloud": false,
                "verboseLevel": "info"
            },
            "outputs": {
                "outputMesh": "{cache}/{nodeType}/{uid0}/mesh.obj",
                "output": "{cache}/{nodeType}/{uid0}/densePointCloud.abc"
            }
        },
        "MeshFiltering_1": {
            "nodeType": "MeshFiltering",
            "position": [
                1395,
                0
            ],
            "parallelization": {
                "blockSize": 0,
                "size": 1,
                "split": 1
            },
            "uids": {
                "0": "ac023a27f374a17dbdea6162054b42a465cfface"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "inputMesh": "{Meshing_1.outputMesh}",
                "removeLargeTrianglesFactor": 60.0,
                "keepLargestMeshOnly": false,
                "iterations": 5,
                "lambda": 1.0,
                "verboseLevel": "info"
            },
            "outputs": {
                "outputMesh": "{cache}/{nodeType}/{uid0}/mesh.obj"
            }
        },
        "Texturing_1": {
            "nodeType": "Texturing",
            "position": [
                1550,
                0
            ],
            "parallelization": {
                "blockSize": 0,
                "size": 1,
                "split": 1
            },
            "uids": {
                "0": "cf5bf7bdd71d153f45e4003aa1eb556e6db5160e"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "input": "{Meshing_1.output}",
                "imagesFolder": "{DepthMap_1.imagesFolder}",
                "inputMesh": "{MeshFiltering_1.outputMesh}",
                "textureSide": 8192,
                "downscale": 2,
                "outputTextureFileType": "png",
                "unwrapMethod": "Basic",
                "useUDIM": true,
                "fillHoles": false,
                "padding": 5,
                "multiBandDownscale": 4,
                "multiBandNbContrib": {
                    "high": 1,
                    "midHigh": 5,
                    "midLow": 10,
                    "low": 0
                },
                "useScore": true,
                "bestScoreThreshold": 0.1,
                "angleHardThreshold": 90.0,
                "processColorspace": "sRGB",
                "correctEV": false,
                "forceVisibleByAllVertices": false,
                "flipNormals": false,
                "visibilityRemappingMethod": "PullPush",
                "subdivisionTargetRatio": 0.8,
                "verboseLevel": "info"
            },
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/",
                "outputMesh": "{cache}/{nodeType}/{uid0}/texturedMesh.obj",
                "outputMaterial": "{cache}/{nodeType}/{uid0}/texturedMesh.mtl",
                "outputTextures": "{cache}/{nodeType}/{uid0}/texture_*.{outputTextureFileTypeValue}"
            }
        }
    }
}