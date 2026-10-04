# Jangan Prototype — Unreal Engine 5.8.3

## Açılış

`JanganPrototype.uproject` dosyasını Unreal Engine 5.8 ile açın.
İlk açılışta shader derleme işleminin bitmesini bekleyin.

- Varsayılan harita: `/Game/Jangan/Maps/Jangan_Day`.
- Gece haritası: `/Game/Jangan/Maps/Jangan_Night`.
- Content Browser içinde `Jangan/Maps` klasöründen haritayı açın.
- Play düğmesi: üçüncü şahıs karakterle dolaşım.
- WASD: hareket, fare: kamera, Space: zıplama, Esc: oyundan çıkış.

## Şehir

Yaklaşık 260 x 280 metre sur içi yerleşim. Güney giriş kapısı,
merkezi altın ejderha meydanı, kuzeyde Daming Palace yorumlaması,
pazar tezgâhları, avlulu konutlar ve köprülü bahçe.

Gece ayrı bir haritadır; otomatik gündüz/gece döngüsü bulunmaz.
Ejderha, kıvrımlı gövdesi, boynuzları, bıyıkları ve pençeleri olan
özgün düşük poligonlu bir heykel prototipidir. Modeller üretim kalitesinde
nihai sanat varlıkları değildir. Silkroad Online oyun varlıkları kullanılmadı.
Üçüncü şahıs karakter ve giriş varlıkları, kurulu Unreal şablonundan alınmıştır.

## Donanım hedefi

8 GB RAM ve RTX 3050 Ti için DX11, Lumen kapalı, sanal gölge haritaları
kapalı, 1024 gölge çözünürlüğü ve %85 render ölçeği ayarlandı.
Bu tercihler FPS garantisi değildir; performans ölçülmelidir.
İlk kullanımda Engine Scalability ayarlarını Medium seçebilirsiniz.

Bu çalışma çevre ve dolaşım prototipidir. MMO sunucusu, görevler,
NPC yapay zekâsı, ekonomi ve kalıcı oyuncu verileri henüz yoktur.

## Doğrulama

İki harita Unreal 5.8.3 ile oluşturuldu, açıldı ve kaydedildi.
Karakter, GameMode ve PlayerController Blueprint'leri editörde derlendi.
Ejderha ve çatının eksenleri, şehir zemini, saray ve oyuncu başlangıç
konumları `validation_report.json` dosyasında kontrol edildi.
`Previews` klasöründeki PNG'ler gerçek Unreal viewport görüntüleridir.
Canlı kullanıcı etkileşimi nedeniyle Play hareket testi ve FPS ölçümü tamamlanmadı.

## Yeniden üretme

`Scripts/build_city.py`, Unreal Python API ile malzemeleri, özgün OBJ
modellerini ve iki haritayı üretir. Bu betik yalnızca üretilmiş haritaları
yeniden oluşturur; el ile yapılan sahne düzenlemeleri önce yedeklenmelidir.
`SourceAssets` kaynak OBJ dosyalarını, `build_report.json` üretim sonucunu içerir.
Model geometrisi betikte değiştirilirse `FORCE_REIMPORT = True` seçilmelidir.
Üretim sırasında aynı projenin başka bir editör kopyası açık olmamalıdır.

Örnek (PowerShell, proje klasöründe):

```powershell
& 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor-Cmd.exe' "$PWD\JanganPrototype.uproject" -run=pythonscript "-script=$PWD\Scripts\build_city.py" -unattended -nullrhi -nosplash
```

Doğu/batı kapıları: Güney kapısının aynı mimarisiyle iki geçiş eklendi. Yan surlar bölündü, doğu-batı yolu uzatıldı. Gündüz/gece kapı merkezleri çarpışma izi ile kontrol edildi. Renkler sıcak taş, kırmızı ahşap ve yeşim çatılarla güncellendi; gökyüzü IsSky ve ortam ışığı ayarları kaydedildi. Güncelleme: Scripts/add_side_gates.py.

NPC yerleşimi: Ejderha–South Gate caddesinin batısında Demirci/Zırhçı/Ahır, doğusunda İksirci/Bakkal/Özel Eşya olmak üzere üçer dükkân. Depocu merkezde; Legends Gate kuzeydoğuda, Oyun Evi doğuda, Avcı Birliği kuzeybatıda. Toplam 10 sabit, geçici Manny NPC; isim ve dükkân tabelaları. Konuşma/alışveriş davranışı henüz yok. Gündüz ve gece haritaları tekrar açılarak animasyon kalıcılığı ve NPC zemini doğrulandı. Scripts/place_npc_shops.py, npc_layout_report.json ve npc_validation.json.

Yerleşim düzeltmesi: Kullanıcı isteğiyle tüm NPC, dükkân ve tabelalar yatay eksende karşı tarafa taşındı. Ejderha–South Gate yönündeki mesafeler ve yükseklikler korundu. Girişler caddeye bakar. Dış sıradaki konut eşleri de takas edilerek üst üste binme önlendi. İki harita kaydedildi; npc_mirror_report.json konumların öncesi/sonrasını içerir.

Kışla: Eski havuz/bahçe ve Avcı Birliği binasının yerine Tang döneminden esinlenen avlulu kışla kuruldu. Komutanlık, iki koğuş, tek çatılı ana kapı, alçak duvarlar, talim zemini, küçük ahır ve su teknesi. Avcı Birliği NPC'si girişe taşındı. Gündüz/gece haritaları kaydedildi; kapı çarpışma izi temiz, avlu zemini engelleme çarpışmasına sahip. Önceki haritalar /Game/Jangan/Backups altında saklı. İnce dekor ve asker davranışları sonraki aşama.

Temple garden: warm ivory/jade/bronze seven-tier pagoda and stylized seated Buddha blockout. Main palace expanded 12% horizontally and 30% above its terrace. Prayer hall removed; organic pond mesh with lotus planting and walkable stepped timber bridge. Both day/night maps saved with BeforeTemple and BeforeOrganicGarden backups. Rebuild includes build_temple.py and refine_temple_garden.py.

Legends monument update: Buddha and its lotus dais moved to the former Legends Gate shop; cyan emissive halo and energy orbs mark the future teleport point (no gameplay teleport configured). Pagoda enlarged 15% horizontally and 10% vertically. Pond shifted 5m inward; bridge shortened 20% and shifted inward. Both approach floors and 26 walking-lane rays verified in each map. update_legends_monument.py is included in rebuild.
