 # Vítejte v aplikaci "Image Reconstruction with Lines"

 ## O aplikaci

Skript slouží k vytváření obrazů pouze přímkami. Jedná se o rekonstrukci dle článku Roberta Reifa:
https://www.robertoreif.com/blog/2018/1/7/drawing-with-straight-lines

Skript obsahuje automatickou kontrolu hodnoty LSE, která ukončí běh při nalezení nejnižší chyby + je přidána možnost 
nastavení tloušťky kreslených přímek.

Výsledky skriptu potvrzují Reifovu analýzu. Nejnižší chyby dosahujeme snížením vzdálenosti mezi kolíky a zmenšením světlosti 
kreslené přímky. Na druhou stranu to však vede k výraznému nárůstu výpočetního času.

<table>
  <tr>
    <td><img src="./images/gradual_formation/Brno-Cathedral-of-St-Peter.jpg" width="270"></td>
    <td><img src="./images/gradual_formation/Brno-Cathedral-of-St-Peter.jpg_PBP-2_GS-2_LSE-0.230_LN-8000_TH-0.png" width="270"></td>
    <td><img src="./images/gradual_formation/Brno-Cathedral-of-St-Peter.jpg_PBP-2_GS-2_LSE-0.149_LN-18000_TH-0.png" width="270"></td>
  </tr>
    <tr>
    <td align="center">originální obrázek</td>
    <td align="center">LSE-0.230_LN-8000</td>
    <td align="center">LSE-0.149_LN-18000</td>
  </tr>
  <tr>
    <td><img src="./images/gradual_formation/Brno-Cathedral-of-St-Peter.jpg_PBP-2_GS-2_LSE-0.086_LN-28000_TH-0.png" width="250"></td>
    <td><img src="./images/gradual_formation/Brno-Cathedral-of-St-Peter.jpg_PBP-2_GS-2_LSE-0.042_LN-38000_TH-0.png" width="250"></td>
    <td><img src="./images/gradual_formation/Brno-Cathedral-of-St-Peter.jpg_PBP-2_GS-2_LSE-0.023_TH-0_LN-44730_ET-19819.png" width="250"></td>
  </tr>
  <tr>
    <td align="center">LSE-0.086_LN-28000</td>
    <td align="center">LSE-0.042_LN-38000</td>
    <td align="center">LSE-0.023_TH-0_LN-44730</td>
  </tr>
</table>

<table>
  <tr>
    <td><img src="./images/gradual_formation/Brno-Cathedral-of-St-Peter.jpg" width="270"></td>
    <td><img src="./images/pixels_between_pegs/Brno-Cathedral-of-St-Peter.jpg_PBP-16_GS-16_LSE-0.037_TH-0_LN-5987_ET-146.png" width="270"></td>
    <td><img src="./images/pixels_between_pegs/Brno-Cathedral-of-St-Peter.jpg_PBP-12_GS-16_LSE-0.031_TH-0_LN-6342_ET-210.png" width="270"></td>
  </tr>
    <tr>
    <td align="center">originální obrázek</td>
    <td align="center">LSE-0.037_LN-5987</td>
    <td align="center">LSE-0.031_LN-6342</td>
  </tr>
  <tr>
    <td><img src="./images/pixels_between_pegs/Brno-Cathedral-of-St-Peter.jpg_PBP-8_GS-16_LSE-0.030_TH-0_LN-6518_ET-291.png" width="250"></td>
    <td><img src="./images/pixels_between_pegs/Brno-Cathedral-of-St-Peter.jpg_PBP-4_GS-16_LSE-0.027_TH-0_LN-6829_ET-569.png" width="250"></td>
    <td><img src="./images/pixels_between_pegs/Brno-Cathedral-of-St-Peter.jpg_PBP-2_GS-16_LSE-0.030_TH-0_LN-6112_ET-1002.png" width="250"></td>
  </tr>
  <tr>
    <td align="center">LSE-0.030_LN-6518</td>
    <td align="center">LSE-0.027_LN-6829</td>
    <td align="center">LSE-0.030_LN-6112</td>
  </tr>
</table>


