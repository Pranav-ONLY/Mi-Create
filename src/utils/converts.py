#shendkarpranav0@proton.me

import os
from PIL import Image, ImageDraw
import torch
import cv2
import numpy as np
from basicsr.archs.srvgg_arch import SRVGGNetCompact
from realesrgan import RealESRGANer

# from ..realesrgan import RealESRGANer

# create a class and use it that way 
class Convert:
    def __init__(self, coreDialog):
        self.dialog = coreDialog
        self.upsampler = None
        self.from_model = self.dialog.fromModelComboBox.currentText()
        self.to_model = self.dialog.toModelComboBox.currentText()
        if self.from_model == self.to_model:
            print("Invalid Conversion, Please select different models to convert between.")
            return
        print(f"Converting from {self.from_model} to {self.to_model}")

        # getting screen resolution
        self.from_res_x, self.from_res_y = self.dialog.models[self.from_model][0]
        self.to_res_x, self.to_res_y = self.dialog.models[self.to_model][0]
        
        # screen resolution for preview image
        self.px, self.py = self.dialog.models[self.to_model][1]

        # device type
        self.dtF = self.dialog.models[self.from_model][2]
        self.dtT = self.dialog.models[self.to_model][2]
        # for checking if deviceTo reuires 8bit images
        self.is_8bit = True if str(self.dtT) in ['12', '3651', '3652'] else False
        # get corner radius
        self.Trad = self.dialog.models[self.to_model][3]
        # dividing screen res to get size difference
        self.x_factor = float(self.to_res_x) / float(self.from_res_x)
        self.y_factor = float(self.to_res_y) / float(self.from_res_y)
        self.mean = float((self.x_factor + self.y_factor)/2)
        print(self.x_factor, self.y_factor, self.dtF, self.dtT)

    def load_up_model(self):
        if self.upsampler is None:
            model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu')
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.upsampler = RealESRGANer(scale=4, model_path='models/realesr-general-wdn-x4v3.pth', model=model, tile=100, tile_pad=10, pre_pad=0, device=device)


    def resizeImageU(self, projectPath, imagePath, newWidth, newHeight):
        try:
            fullPath = os.path.join(os.path.dirname(projectPath), f"images/{imagePath}")
            if not os.path.exists(fullPath):
                return
            img = cv2.imread(fullPath, cv2.IMREAD_UNCHANGED)
            if img is None:
                try:
                    pil_image = Image.open(fullPath).convert('RGBA')
                    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGBA2BGRA)
                except Exception as e:
                    print(f"Error loading {imagePath} with Pillow: {str(e)}")
                    return
            img_height, img_width = img.shape[:2]
            if img_width < 30 and img_height < 30:
                final = cv2.resize(img, (newWidth, newHeight), interpolation=cv2.INTER_LANCZOS4)
                final = cv2.cvtColor(final, cv2.COLOR_BGRA2RGBA)
                Image.fromarray(final).save(fullPath)
                return
            else:
                output, _ = self.upsampler.enhance(img)
                output_rgba = cv2.cvtColor(output, cv2.COLOR_BGRA2RGBA)
                pil_image = Image.fromarray(output_rgba, 'RGBA')
                resized_img = pil_image.resize((newWidth, newHeight), Image.LANCZOS)
                if self.is_8bit:
                    eight_bit_img = resized_img.convert("P", palette=Image.ADAPTIVE, colors=256)
                    eight_bit_img.save(fullPath)
                else:
                    resized_img.save(fullPath)
        except Exception as e:
            print(f"Error processing {imagePath}: {str(e)}")  

    def resizeImageD(self, projectPath, imagePath, newWidth, newHeight):   #pillow
        fullPath = os.path.join(os.path.dirname(projectPath), f"images/{imagePath}")
        if os.path.exists(fullPath):
            with Image.open(fullPath) as img:
                resized_img = img.resize((newWidth, newHeight), Image.LANCZOS)
                if self.is_8bit:
                    eight_bit_img = resized_img.convert("P", palette=Image.ADAPTIVE, colors=256)
                    eight_bit_img.save(fullPath)  
                else:
                    resized_img.save(fullPath)


    def cutBGcorner(self, projectPath, imagePath):
        fullPath = os.path.join(os.path.dirname(projectPath), f"images/{imagePath}")
        if os.path.exists(fullPath):
            with Image.open(fullPath) as img:
                large_mask = Image.new("L", ((img.width * 4), (img.height * 4)), 0)
                draw = ImageDraw.Draw(large_mask)
                draw.rounded_rectangle((0, 0, (img.width * 4), (img.height * 4)), radius=self.Trad * 4, fill=255)
                mask = large_mask.resize(img.size, Image.LANCZOS)
                rounded_img = Image.new("RGBA", img.size)
                rounded_img.paste(img, mask=mask)
                if self.is_8bit:
                    eight_bit_img = rounded_img.convert("P", palette=Image.ADAPTIVE, colors=256)
                    eight_bit_img.save(fullPath)  
                else:
                    rounded_img.save(fullPath)

    def projectDataConversion(self, project):
        # Update DeviceType
        if str(project.data['FaceProject']['@DeviceType']) == str(self.dtF):
            project.data['FaceProject']['@DeviceType'] = str(self.dtT)
        else:
            return
        if str(project.data['FaceProject']['Screen']['@Bitmap']) != '':
            self.resizeImage(project.dataPath, project.data['FaceProject']['Screen']['@Bitmap'], int(self.px), int(self.py))
            self.cutBGcorner(project.dataPath, project.data['FaceProject']['Screen']['@Bitmap'])

        
        # Process each Widget
        widgets = project.data['FaceProject']['Screen']['Widget']
        if not isinstance(widgets, list):
            widgets = [widgets]  # Ensure widgets is a list

        self.dialog.progressBar.setMaximum(len(widgets))
        self.dialog.progressBar.setValue(0)
        # for RW3A
        if str(self.dtT) == "12":
            self.RW3A(widgets, project)
           
        for i, widget in enumerate(widgets):
            # Update X and Y coordinates
            widget['@X'] = str(round(float(widget['@X']) * self.x_factor))
            widget['@Y'] = str(round(float(widget['@Y']) * self.y_factor))
                        
            self.dialog.progressBar.setValue(i + 1) # for small progressbar
            # Update Width and Height
            if '@Digits' in widget and (int(widget['@Digits'])>1):
                try:
                    firstImagePath = widget['@BitmapList'].split('|')[0]
                    mainPath = os.path.join(os.path.dirname(project.dataPath), f"images/{firstImagePath}")
                    if os.path.exists(mainPath):
                        with Image.open(mainPath) as img:
                            if img.width == int(widget['@Width']):
                                widget['@Width'] = str(round(float(widget['@Width']) * self.x_factor))
                            elif img.width == round(float(widget['@Width']) * self.x_factor):
                                widget['@Width'] = str(round(float(widget['@Width']) * self.x_factor))
                            elif int(widget['@Spacing']) == 0:
                                widget['@Width'] = str(round(float(int(widget['@Width'])/int(widget['@Digits'])) * self.x_factor))
                            else:
                                widget['@Width'] = str(round(float( int(widget['@Width']) + int(widget['@Digits']) + int(widget['@Spacing']) ) / int(widget['@Digits'])  * self.x_factor))
                except FileNotFoundError:
                    print(f"Image not found: {firstImagePath}")
            else:
                widget['@Width'] = str(round(float(widget['@Width']) * self.x_factor))

            widget['@Height'] = str(round(float(widget['@Height']) * self.y_factor))
            
            # Resize images
            if '@Bitmap' in widget:
                self.resizeImage(project.dataPath, widget['@Bitmap'], int(widget['@Width']), int(widget['@Height']))
                if int(widget['@Width']) == self.to_res_x and int(widget['@Height']) == self.to_res_y:
                    self.cutBGcorner(project.dataPath, widget['@Bitmap'])

            elif '@BitmapList' in widget:
                for bitmap in widget['@BitmapList'].split('|'):
                    if bitmap == "":
                        break
                    self.resizeImage(project.dataPath, bitmap.split(':')[1] if ':' in bitmap else bitmap, int(widget['@Width']), int(widget['@Height']))
            
            elif widget['@Shape'] == '42':
                widget['@Rotate_xc'] = round(int(widget['@Rotate_xc']) * self.mean)
                widget['@Rotate_yc'] = round(int(widget['@Rotate_yc']) * self.mean)
                widget['@Radius'] = round(int(widget['@Radius']) * self.mean)
                widget['@Line_Width'] = round(int(widget['@Line_Width']) * self.mean)

                if widget['@Background_ImageName'] != "":
                    img_path =  os.path.join(os.path.dirname(project.dataPath), f"images/{widget['@Background_ImageName']}")
                    if os.path.exists(img_path):
                        with Image.open(img_path) as imgCbg:
                            newWidthCbg = round(float(imgCbg.width) * self.mean)
                            newHeightCbg = round(float(imgCbg.height) * self.mean)
                            self.resizeImage(project.dataPath, widget['@Background_ImageName'], newWidthCbg, newHeightCbg)

                if widget['@Foreground_ImageName'] != "":
                    img_path =  os.path.join(os.path.dirname(project.dataPath), f"images/{widget['@Foreground_ImageName']}")
                    if os.path.exists(img_path):
                        with Image.open(img_path) as imgC:
                            newWidthC = round(float(imgC.width) * self.mean)
                            newHeightC = round(float(imgC.height) * self.mean)
                            self.resizeImage(project.dataPath, widget['@Foreground_ImageName'], newWidthC, newHeightC)
                
            elif '@HourHand_ImageName' in widget and str(widget['@HourHand_ImageName']) != '':
                img_path =  os.path.join(os.path.dirname(project.dataPath), f"images/{widget['@HourHand_ImageName']}")
                if os.path.exists(img_path):
                    with Image.open(img_path) as imgH:
                        newWidthH = round(float(imgH.width) * self.mean)
                        newHeightH = round(float(imgH.height) * self.mean)
                        self.resizeImage(project.dataPath, widget['@HourHand_ImageName'], newWidthH, newHeightH)

                widget['@HourImage_rotate_xc'] = round((float(widget['@HourImage_rotate_xc'])*self.mean))
                widget['@HourImage_rotate_yc'] = round((float(widget['@HourImage_rotate_yc'])*self.mean))

            if '@MinuteHand_Image' in widget and str(widget['@MinuteHand_Image']) != '':
                img_path =  os.path.join(os.path.dirname(project.dataPath), f"images/{widget['@MinuteHand_Image']}")
                if os.path.exists(img_path):
                    with Image.open(img_path) as imgM:
                        newWidthM = round(float(imgM.width) * self.mean)
                        newHeightM = round(float(imgM.height) * self.mean)
                        self.resizeImage(project.dataPath, widget['@MinuteHand_Image'], newWidthM, newHeightM)

                widget['@MinuteImage_rotate_xc'] = round((float(widget['@MinuteImage_rotate_xc'])*self.mean))
                widget['@MinuteImage_rotate_yc'] = round((float(widget['@MinuteImage_rotate_yc'])*self.mean))

            if '@SecondHand_Image' in widget and str(widget['@SecondHand_Image']) != '':
                img_path =  os.path.join(os.path.dirname(project.dataPath), f"images/{widget['@SecondHand_Image']}")
                if os.path.exists(img_path):
                    with Image.open(img_path) as imgS:
                        newWidthS = round(float(imgS.width) * self.mean)
                        newHeightS = round(float(imgS.height) * self.mean)
                        self.resizeImage(project.dataPath, widget['@SecondHand_Image'], newWidthS, newHeightS)
                widget['@SecondImage_rotate_xc'] = round((float(widget['@SecondImage_rotate_xc'])*self.mean))
                widget['@SecondImage_rotate_yc'] = round((float(widget['@SecondImage_rotate_yc'])*self.mean))

    def resizeImage(self, projectPath, imagePath, newWidth, newHeight):
        scale_factor = max(self.x_factor, self.y_factor)  # Use the larger scale to determine upscaling or downscaling
        if scale_factor > 1:
            self.load_up_model()
            self.resizeImageU(projectPath, imagePath, newWidth, newHeight)  # Upscaling
        else:
            self.resizeImageD(projectPath, imagePath, newWidth, newHeight) # Downscaling
    
    def RW3A(self, widgets, project):
        if str(widgets[0]['@Shape']) != '30':
            first_img = Image.new("RGB", (1, 1), (0, 0, 0))
            first_img_path = os.path.join(os.path.dirname(project.dataPath), f"images/first_bg.png")
            first_img.save(first_img_path)
            first_img_widget = {'@Shape': '30', '@Name': 'background', '@X': '0', '@Y': '0', '@Width': '1', '@Height': '1', '@Alpha': '255', '@Visible_Src': '0', '@Bitmap': 'first_bg.png'}
            widgets.insert(0, first_img_widget)
        # prefixRW3A = {1012:'0D', 1812:'0F', 2012:'11', 1000911:'38', 911:'39', 1211:'3B', 1111:'3C', 841:'09', 821:'1C', 823:'27', 822:'31'}
        data_src ={'811':('hour', '42'),
                '911':('hourLow', '39'),
                '1000911':('hourHigh', '38'),
                '1011':('minute', '43'),
                '1111':('minLow', '3C'),
                '1211':('minHigh', '3B'),
                '1811':('second', '44'),
                '1911':('secLow', '00'),
                '1001911':('secHigh', '00'),
                '1812':('day', '0F'),
                '1912':('dayLow', '00'),
                '1001912':('dayHigh', '00'),
                '2012':('week', '11'),
                '1012':('month', '0D'),
                '812':('year', '00'),
                '813':('isAM', '14'),
                '1013':('isPM', '15'),
                '3031':('weatherIcon', '00'),
                '841':('batt', '09'),
                '1841':('sleepStatus', '00'),
                '2041':('btStatus', '00'),
                '3041':('lockStatus', '00'),
                '822':('hrm', '31'),
                '1022':('intHrm', '00'),
                '821':('steps', '1C'),
                '1021':('stepsPercent', '18'),
                '823':('calories', '27'),
                '1023':('calPercent', '23'),
                '824':('stand', '00'),
                '826':('stress', '00'),
                '5031':('weatherSomething', '00'),
                '828':('sleepScrore', '00')}
        
        for i, wid in enumerate(widgets[1:]): # for watch 3 active color checking and naming
            if str(wid['@Shape']) == '31':
                first_Image_Path = wid['@BitmapList'].split('|')[0].split(':')[1]
                mainPath = os.path.join(os.path.dirname(project.dataPath), f"images/{first_Image_Path}")
                if os.path.exists(mainPath):
                    with Image.open(mainPath) as f_img:
                            if f_img.mode == "RGB":
                                r, g, b = f_img.resize((1, 1)).getpixel((0, 0))
                            elif f_img.mode == "RGBA":
                                r, g, b, _ = f_img.resize((1, 1)).getpixel((0, 0))
                            hex_rgb = f"{r:02x}{g:02x}{b:02x}"  
                if wid['@Index_Src'] == '0A11':
                    wid['@Index_Src'] = '1000911'

                if int(wid['@Index_Src']) == '841':
                    wid['@Name'] = f'04_imgList_{data_src[str(int(wid['@Index_Src']))][0]}_color[{hex_rgb}]'
                elif str(int(wid['@Index_Src'])) in data_src:
                    wid['@Name'] = f'{data_src[str(int(wid['@Index_Src']))][1]}_imgList_{data_src[str(int(wid['@Index_Src']))][0]}_color[{hex_rgb}]'
                else:
                    wid['@Name'] = f'0{i}_imglist_color[{hex_rgb}]'
            elif str(wid['@Shape']) == '32':
                first_Image_Path = wid['@BitmapList'].split('|')[0]
                mainPath = os.path.join(os.path.dirname(project.dataPath), f"images/{first_Image_Path}")
                if os.path.exists(mainPath):
                    with Image.open(mainPath) as f_img:
                            if f_img.mode == "RGB":
                                r, g, b = f_img.resize((1, 1)).getpixel((0, 0))
                            elif f_img.mode == "RGBA":
                                r, g, b, _ = f_img.resize((1, 1)).getpixel((0, 0))
                            hex_rgb = f"{r:02x}{g:02x}{b:02x}" 
                if wid['@Value_Src'] == '0A11':
                    wid['@Value_Src'] = '1000911'
                if str(int(wid['@Value_Src'])) in data_src:
                    wid['@Name'] = f'{data_src[str(int(wid['@Value_Src']))][1]}_num_{data_src[str(int(wid['@Value_Src']))][0]}_color[{hex_rgb}]'
                else:
                    wid['@Name'] = f'0{i}_num_color[{hex_rgb}]'
            elif str(wid['@Shape']) == '30':
                first_Image_Path = wid['@Bitmap']
                mainPath = os.path.join(os.path.dirname(project.dataPath), f"images/{first_Image_Path}")
                if os.path.exists(mainPath):
                    with Image.open(mainPath) as f_img:
                            if f_img.mode == "RGB":
                                r, g, b = f_img.resize((1, 1)).getpixel((0, 0))
                            elif f_img.mode == "RGBA":
                                r, g, b, a = f_img.resize((1, 1)).getpixel((0, 0))
                            hex_rgb = f"{r:02x}{g:02x}{b:02x}" 
                wid['@Name'] = f'0{i}_img_color[{hex_rgb}]'
            else:
                wid['@Name'] = f'0{i}_none'