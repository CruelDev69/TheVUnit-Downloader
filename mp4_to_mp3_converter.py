'''
MIT License

Copyright (c) 2022 Ahad 

If you want to use this code for any purpose, kindly give credits before using. 
You can modify or edit it but you are not allowed to remove the author name 
from the code.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from moviepy.editor import * # Importing moviepy module.
import os # importing os module
from colorama import Fore # Importing colorama

print(Fore.RED + '''
╦  ╦┬┌┬┐┌─┐┌─┐  ╔╦╗┌─┐  ╔═╗┬ ┬┌┬┐┬┌─┐  ╔═╗┌─┐┌┐┌┬  ┬┌─┐┬─┐┌┬┐┌─┐┬─┐
╚╗╔╝│ ││├┤ │ │   ║ │ │  ╠═╣│ │ ││││ │  ║  │ ││││└┐┌┘├┤ ├┬┘ │ ├┤ ├┬┘
 ╚╝ ┴─┴┘└─┘└─┘   ╩ └─┘  ╩ ╩└─┘─┴┘┴└─┘  ╚═╝└─┘┘└┘ └┘ └─┘┴└─ ┴ └─┘┴└─
''' + Fore.RESET)
print(Fore.YELLOW + '''
Author: Ahad#3257                            
Website: https://itscruel.cf
Github: https://github.com/CruelDev69/YouTube-Video-Downloader
''' + Fore.RESET)

vidName = input(Fore.BLUE + "Make sure the name of video you enter is present in this directory.\nEnter a mp4 video's name to convert it to mp3: ") # Requiring name of mp4 file

video = VideoFileClip(os.path.join(os.getcwd(),f'{vidName}.mp4')) # Getting mp4 file.
video.audio.write_audiofile(os.path.join(os.getcwd(),f"{vidName}_converted.mp3")) # Converting mp4 file to mp3.