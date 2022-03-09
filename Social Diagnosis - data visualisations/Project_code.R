#-----------------------------zaladowanie pakietow --------------------------------------
library(haven)
library(dplyr)
library(label)
library(sjlabelled)
library(ggplot2)
library(ggthemes)
library(OIdata)
library(ggpubr)
library(tidyverse)
library(labelled) 
library(surveytoolbox) # install with devtools::install_github("martinctc/surveytoolbox")
library(gdata)



#---------------------------przygotowanie zbioru----------------------------------------

my_colors <- RColorBrewer::brewer.pal(11,"RdBu")[c(9,4,2,1)]
column_color <- RColorBrewer::brewer.pal(9,"Blues")[7]

path2 <- "C:/Users/patry/Downloads/ds_0_15_ind_14112015.sav"
indywidualny <- read_sav(path2)

indywidualny_bez_null <- indywidualny[!is.na(indywidualny$HP52) & !is.na(indywidualny$HP52) , ]
indywidualny_bez_null <- as.data.frame(indywidualny_bez_null)

indywidualny_bez_null$BMI <- indywidualny_bez_null$HP53 / (indywidualny_bez_null$HP52/100)^2

indywidualny_bez_null$BMI_ocena <- ifelse(indywidualny_bez_null$BMI >= 25, 
                                          ifelse(indywidualny_bez_null$BMI>=30, 'otyłość','nadwaga'),
                                          ifelse(indywidualny_bez_null$BMI<18.5,'niedowaga','prawidłowa'))





#-----------------------------PYTANIE 3-----------------------------------------------
#sekcja ---> odczucia

Pytanie3 <- indywidualny_bez_null %>%
  mutate(HP3 = as_factor(HP3)) %>% 
  group_by(BMI_ocena, HP3) %>% count()
Pytanie3 <- Pytanie3[!is.na(Pytanie3$HP3),]

levels(Pytanie3$HP3) <- gsub(" ", "\n", levels(Pytanie3$HP3))
levels(Pytanie3$HP3)
levels(Pytanie3$HP3)[5] <- "ANI DOBRE,\nANI ZŁE"


#---------nadwaga---------------
Pytanie3_nadwaga <- Pytanie3
Pytanie3_nadwaga$n <- (Pytanie3$n/sum(na.omit(Pytanie3[Pytanie3$BMI_ocena=='nadwaga' & !is.na(Pytanie3$HP3),]$n)))*100
Pytanie3_nadwaga <- Pytanie3_nadwaga[Pytanie3_nadwaga$BMI_ocena=='nadwaga' & !is.na(Pytanie3_nadwaga$HP3),]
Pytanie3_nadwaga <- Pytanie3_nadwaga[1:6,]


plot3_a <- ggplot(Pytanie3_nadwaga[Pytanie3_nadwaga$BMI_ocena == 'nadwaga', ], aes(x = HP3, y = n)) +
  geom_col(fill = column_color) +
  theme_economist_white() + 
  xlab("") + 
  ylab("Procent ankietowanych") +
  theme(axis.title.y = element_text(color="black", size=14, face="bold",
                                    margin = margin(t = 0, r = 12, b = 0, l = 0))) +
  theme(axis.text.x = element_text(color="black", size=10, face="bold",
                                   vjust = 0.7)) +
  geom_text(aes(label = paste( sprintf("%0.2f",round(n,digits=3)),'%')), nudge_x = 0, vjust=-0.7,
            colour = "black", fontface = "bold")+
  scale_y_continuous(limits = c(0,43)) +
  ggtitle("OSOBY Z NADWAGĄ") +
  theme(plot.title = element_text(hjust=0.5, vjust = 1.9, size = 12))


#---------prawidlowa---------------
Pytanie3_praw <- Pytanie3
Pytanie3_praw$n <- (Pytanie3_praw$n/sum(na.omit(Pytanie3_praw[Pytanie3_praw$BMI_ocena=='prawidłowa'
                                                              & !is.na(Pytanie3_praw$HP3),]$n)))*100
Pytanie3_praw <- Pytanie3_praw[Pytanie3_praw$BMI_ocena=='prawidłowa' & !is.na(Pytanie3_praw$HP3),]
Pytanie3_praw <- Pytanie3_praw[1:6,]


plot3_b <- ggplot(Pytanie3_praw[Pytanie3_praw$BMI_ocena == 'prawidłowa', ], aes(x = HP3, y = n)) +
  geom_col(fill = column_color) +
  theme_economist_white() + 
  xlab("") + 
  ylab("Procent ankietowanych") +
  theme(axis.title.y = element_text(color="black", size=14, face="bold",
                                    margin = margin(t = 0, r = 12, b = 0, l = 0))) +
  theme(axis.text.x = element_text(color="black", size=10, face="bold",
                                   vjust = 0.7)) +
  geom_text(aes(label = paste( sprintf("%0.2f",round(n,digits=3)),'%')), nudge_x = 0, vjust=-0.7,
            colour = "black", fontface = "bold")+
  scale_y_continuous(limits = c(0,43)) +
  ggtitle("OSOBY Z PRAWIDŁOWYM BMI") +
  theme(plot.title = element_text(hjust=0.5, vjust = 1.9, size = 12))



#---------niedowaga---------------
Pytanie3_niedow <- Pytanie3
Pytanie3_niedow$n <- (Pytanie3_niedow$n/sum(na.omit(Pytanie3_niedow[Pytanie3_niedow$BMI_ocena=='niedowaga' 
                                                                    & !is.na(Pytanie3_niedow$HP3),]$n)))*100
Pytanie3_niedow <- Pytanie3_niedow[Pytanie3_niedow$BMI_ocena=='niedowaga' & !is.na(Pytanie3_niedow$HP3),]
Pytanie3_niedow <- Pytanie3_niedow[1:6,]


plot3_c <- ggplot(Pytanie3_niedow[Pytanie3_niedow$BMI_ocena == 'niedowaga', ], aes(x = HP3, y = n)) +
  geom_col(fill = column_color) +
  theme_economist_white() + 
  xlab("") + 
  ylab("Procent ankietowanych") +
  theme(axis.title.y = element_text(color="black", size=14, face="bold",
                                    margin = margin(t = 0, r = 12, b = 0, l = 0))) +
  theme(axis.text.x = element_text(color="black", size=10, face="bold",
                                   vjust = 0.7)) +
  geom_text(aes(label = paste( sprintf("%0.2f",round(n,digits=3)),'%')), nudge_x = 0, vjust=-0.7,
            colour = "black", fontface = "bold")+
  scale_y_continuous(limits = c(0,43)) +
  ggtitle("OSOBY Z NIEDOWAGĄ") +
  theme(plot.title = element_text(hjust=0.5, vjust = 1.9, size = 12))



#---------otylosc---------------
Pytanie3_otyl <- Pytanie3
Pytanie3_otyl$n <- (Pytanie3_otyl$n/sum(na.omit(Pytanie3_otyl[Pytanie3_otyl$BMI_ocena=='otyłość' 
                                                              & !is.na(Pytanie3_otyl$HP3),]$n)))*100
Pytanie3_otyl <- Pytanie3_otyl[Pytanie3_otyl$BMI_ocena=='otyłość' & !is.na(Pytanie3_otyl$HP3),]
Pytanie3_otyl <- Pytanie3_otyl[1:6,]


plot3_d <- ggplot(Pytanie3_otyl[Pytanie3_otyl$BMI_ocena == 'otyłość', ], aes(x = HP3, y = n)) +
  geom_col(fill = column_color) +
  theme_economist_white() + 
  xlab("") + 
  ylab("Procent ankietowanych") +
  theme(axis.title.y = element_text(color="black", size=14, face="bold",
                                    margin = margin(t = 0, r = 12, b = 0, l = 0))) +
  theme(axis.text.x = element_text(color="black", size=10, face="bold",
                                   vjust = 0.7)) +
  geom_text(aes(label = paste( sprintf("%0.2f",round(n,digits=3)),'%')), nudge_x = 0, vjust=-0.7,
            colour = "black", fontface = "bold")+
  scale_y_continuous(limits = c(0,43)) +
  ggtitle("OSOBY Z OTYŁOŚCIĄ") +
  theme(plot.title = element_text(hjust=0.5, vjust = 1.9, size = 12))


#---------komentarz przed wykresem---------------
# Analizę różnic pomiędzy poszczególnymi kategoriami masy ciała warto zacząć od porównania 
# ogólnej oceny ich dotychczasowego życia. Adekwatnym do tego tematu pytaniem będzie pytanie
# nr 3 z kwestionariusza indywidualnego. Treść pytania brzmi:
# "Jak ocenia Pan swoje całe dotychczasowe życie, czy mógłby Pan powiedzieć, że było?".
# Ankietowani mieli do wyboru 6 odpowiedzi, które widoczne są na osi poziomej każdego z
# wykresów.


#---------glowny wykres---------------
ggarrange(plot3_c, plot3_b, plot3_a, plot3_d, 
          labels = c("", "", "", ""),
          ncol = 2, nrow = 2)+
#  ggtitle("Jak ocenia Pan swoje całe dotychczasowe życie, czy mógłby Pan powiedzieć, że było? ") +
  theme(plot.title = element_text(hjust=0.5, vjust = 1,
                                  size = 17, face = "bold"))

#---------komentarz po wykresie---------------
# Na podstawie powyższych wykresów można stwierdzić, że odpowiedzi dla poszczególnych
# kategorii masy ciała są podobne. Niewielkie różnice widoczne są dla
# osób z niedowagą, które częściej wskazywały, że ich dotychczasowe życie
# było wspaniałe lub udane. Z kolei osoby z otyłością najrzadziej zaznaczały
# wspomniane odpowiedzi, wykazując swoje niezdecydowanie w ocenie swojego
# życia. 

#----------------------------- ***************************** ---------------------------


#-----------------------------PYTANIE 62_12-----------------------------------------------
#sekcja ----> zdrowie

Pytanie62_12 <- indywidualny_bez_null %>%
  mutate(HP62_12 = as_factor(HP62_12)) %>% 
  group_by(BMI_ocena, HP62_12) %>% count()

c("niedowaga","prawidłowa", "nadwaga", "otyłość")

Pytanie62_12$BMI_ocena <- reorder.factor(Pytanie62_12$BMI_ocena, 
                                         new.order=c("niedowaga","prawidłowa", "nadwaga", "otyłość"))

Pytanie62_12 %>% arrange(BMI_ocena)
levels(Pytanie62_12$HP62_12)[3] <- "MIEWAŁ RZADZIEJ NIŻ\nPRZEZ 15 DNI"
levels(Pytanie62_12$HP62_12)[4] <- "MIEWAŁ CO NAJMNIEJ\nPRZEZ POŁOWĘ MIESIĄCA"
Pytanie62_12 <- Pytanie62_12[!is.na(Pytanie62_12$HP62_12) & 
                               !is.na(Pytanie62_12$BMI_ocena),]


#---------komentarz przed wykresem---------------
# W tej sekcji sprawdzimy, czy masa ciała ma wpływ na uczucie zmęczenia niezwiązanego z pracą.
# Na wykresie każdy słupek przedstawia strukturę odpowiedzi na pytanie obrazujące temat analizy 
# w tej sekcji dla poszczególnych kategorii wyznaczonych na podstawie wskaźnika BMI.


#---------glowny wykres---------------

ggplot(Pytanie62_12, aes(fill = HP62_12, y = n, x = BMI_ocena)) +
  geom_bar(position="fill", stat="identity") +
  scale_x_discrete(labels = c("niedowaga", "prawidłowa", "nadwaga", "otyłość")) +
  xlab("Kategoria masy ciała na podstawie wskaźnika BMI") +
  ylab("Udział w całości") +
  scale_fill_manual(values = my_colors, name = "Czy w okresie minionego miesiąca zdarzało się Panu\n doświadczać uczucia zmęczenia niezwiązanego z pracą?",
                    labels = c("Nie miałem",
                               "Miewałem rzadziej niż przez 15 dni",
                               "Miewałem co najmniej przez połowę miesiąca")) +
  theme(title = element_text(hjust=0.5, vjust = 1.9, size = 11, face = "bold"),
        plot.subtitle = element_text(hjust=0.5, vjust = 1, size = 14)) +
  theme(axis.text.x = element_text(color="black", size=11,
                                   vjust = 0.7))


# ---------komentarz po wykresie---------------
# Możemy zauważyć, że dla osób z niedowagą i prawidłowym BMI struktura jest bardzo podobna.
# Jednakże osoby o wyższym wskażniku BMI, szczególnie te z otyłością, częściej doświadczały 
# uczucia zmęczenia niezwiązanego z pracą w ciągu minionego miesiąca. 

#----------------------------- ***************************** ---------------------------



#-----------------------------------PYTANIE 62_03 --------------------------------------
#sekcja ----> zdrowie

Pytanie62_03 <- indywidualny_bez_null%>%
  mutate(HP62_03 = as_factor(HP62_03)) %>% 
  group_by(BMI_ocena, HP62_03) %>% count()

levels(Pytanie62_03$HP62_03)[3] <- "MIEWAŁ RZADZIEJ NIŻ\nPRZEZ 15 DNI"
levels(Pytanie62_03$HP62_03)[4] <- "MIEWAŁ CO NAJMNIEJ\nPRZEZ POŁOWĘ MIESIĄCA"

Pytanie62_03$BMI_ocena <- reorder.factor(Pytanie62_03$BMI_ocena, 
                                         new.order=c("niedowaga","prawidłowa", "nadwaga", "otyłość"))

Pytanie62_03 %>% arrange(BMI_ocena)
Pytanie62_03 <- Pytanie62_03[!is.na(Pytanie62_03$HP62_03) & 
                               !is.na(Pytanie62_03$BMI_ocena),]


#---------komentarz przed wykresem---------------
# Sprawdzimy teraz czy osoby w poszczególnych kategorii masy ciała
# w różnej częstotliwości odczuwają bóle mięśni. W tym przypadku
# analiza dotyczy pytania o bóle albo napięcia mięśni karku i ramion.


#---------glowny wykres---------------
tresc_62_03 <- "Czy w okresie minionego miesiąca zdarzyło się Panu doświadczyć\n uczucia bólu albo napięcia mięśni karku i ramion?"

ggplot(Pytanie62_03, aes(fill = HP62_03, y = n, x = BMI_ocena)) +
  geom_bar(position="fill", stat="identity") +
  scale_x_discrete(labels = c("niedowaga", "prawidłowa", "nadwaga", "otyłość")) +
  xlab("Kategoria masy ciała na podstawie wskaźnika BMI") +
  ylab("Udział w całości") +
  scale_fill_manual(values = my_colors, name = tresc_62_03,
                    labels = c("Nie miałem",
                               "Miewałem rzadziej niż przez 15 dni",
                               "Miewałem co najmniej przez połowę miesiąca")) +
  theme(title = element_text(hjust=0.5, vjust = 1.9, size = 11, face = "bold")) +
  theme(axis.text.x = element_text(color="black", size=11,
                                   vjust = 0.7))


#---------komentarz po wykresie---------------
# Na podstawie tego wykresu możemy wywnioskować, że rzeczywiście masa człowieka, 
# a dokładnie jej kategoria wyznaczona na podstawie wskaźnika BMI ma wpływ na 
# częstotliwość uczucia bólu mięśni karku i ramion.
# W okresie minionego miesiąca zdecydowanie najczęściej doświadczały go
# osoby z otyłością i z nadwagą, a najrzadziej osoby z niedowagą.

#----------------------------- ***************************** ---------------------------


#-----------------------------------PYTANIE 57_12 --------------------------------------
#sekcja ---> odczucia

Pytanie57_12 <- indywidualny_bez_null %>% 
  mutate(HP57_12 = as_factor(HP57_12)) %>% 
  group_by(BMI_ocena, HP57_12) %>% count()

levels(Pytanie57_12$HP57_12) <- gsub(" ", "\n", levels(Pytanie57_12$HP57_12))
levels(Pytanie57_12$HP57_12)[5] <- "ANI TAK,\nANI NIE"


#---------nadwaga---------------

Pytanie57_12_nadwaga <- Pytanie57_12
Pytanie57_12_nadwaga$n <- (Pytanie57_12_nadwaga$n/sum(na.omit(
  Pytanie57_12_nadwaga[Pytanie57_12_nadwaga$BMI_ocena=='nadwaga'
                       & !is.na(Pytanie57_12_nadwaga$HP57_12),]$n)))*100
Pytanie57_12_nadwaga <- Pytanie57_12_nadwaga[Pytanie57_12_nadwaga$BMI_ocena=='nadwaga' & 
                                               !is.na(Pytanie57_12_nadwaga$HP57_12),]
Pytanie57_12_nadwaga <- Pytanie57_12_nadwaga[1:7,]


plot57_12_a <- ggplot(Pytanie57_12_nadwaga, aes(x = HP57_12, y = n)) +
  geom_col(fill = column_color) +
  theme_economist_white() + 
  xlab("") + 
  ylab("Procent ankietowanych") +
  theme(axis.title.y = element_text(color="black", size=14, face="bold",
                                    margin = margin(t = 0, r = 12, b = 0, l = 0))) +
  geom_text(aes(label = paste( sprintf("%0.2f",round(n,digits=3)),'%')), nudge_x = 0, vjust=-0.7,
            colour = "black", fontface = "bold")+
  theme(axis.text.x = element_text(color="black", size=10, face="bold",
                                   vjust = 0.7)) +
  scale_y_continuous(limits = c(0,43)) +
  ggtitle("OSOBY Z NADWAGĄ") +
  theme(plot.title = element_text(hjust=0.5, vjust = 1.9, size = 12))


#---------prawidlowa---------------
Pytanie57_12_praw <- Pytanie57_12
Pytanie57_12_praw$n <- (Pytanie57_12_praw$n/sum(na.omit(
  Pytanie57_12_praw[Pytanie57_12_praw$BMI_ocena=='prawidłowa'
                    & !is.na(Pytanie57_12_praw$HP57_12),]$n)))*100
Pytanie57_12_praw <- Pytanie57_12_praw[Pytanie57_12_praw$BMI_ocena=='prawidłowa' & 
                                         !is.na(Pytanie57_12_praw$HP57_12),]
Pytanie57_12_praw <- Pytanie57_12_praw[1:7,]


plot57_12_b <- ggplot(Pytanie57_12_praw, aes(x = HP57_12, y = n)) +
  geom_col(fill = column_color) +
  theme_economist_white() + 
  xlab("") + 
  ylab("Procent ankietowanych") +
  theme(axis.title.y = element_text(color="black", size=14, face="bold",
                                    margin = margin(t = 0, r = 12, b = 0, l = 0))) +
  geom_text(aes(label = paste( sprintf("%0.2f",round(n,digits=3)),'%')), nudge_x = 0, vjust=-0.7,
            colour = "black", fontface = "bold")+
  theme(axis.text.x = element_text(color="black", size=10, face="bold",
                                   vjust = 0.7)) +
  scale_y_continuous(limits = c(0,43)) +
  ggtitle("OSOBY Z PRAWIDŁOWYM BMI") +
  theme(plot.title = element_text(hjust=0.5, vjust = 1.9, size = 12))


#---------niedowaga---------------
Pytanie57_12_niedow <- Pytanie57_12
Pytanie57_12_niedow$n <- (Pytanie57_12_niedow$n/sum(na.omit(
  Pytanie57_12_niedow[Pytanie57_12_niedow$BMI_ocena=='niedowaga'
                      & !is.na(Pytanie57_12_niedow$HP57_12),]$n)))*100
Pytanie57_12_niedow <- Pytanie57_12_niedow[Pytanie57_12_niedow$BMI_ocena=='niedowaga' & 
                                             !is.na(Pytanie57_12_niedow$HP57_12),]
Pytanie57_12_niedow <- Pytanie57_12_niedow[1:7,]


plot57_12_c <- ggplot(Pytanie57_12_niedow, aes(x = HP57_12, y = n)) +
  geom_col(fill = column_color) +
  theme_economist_white() + 
  xlab("") + 
  ylab("Procent ankietowanych") +
  theme(axis.title.y = element_text(color="black", size=14, face="bold",
                                    margin = margin(t = 0, r = 12, b = 0, l = 0))) +
  geom_text(aes(label = paste( sprintf("%0.2f",round(n,digits=3)),'%')), nudge_x = 0, vjust=-0.7,
            colour = "black", fontface = "bold")+
  theme(axis.text.x = element_text(color="black", size=10, face="bold",
                                   vjust = 0.7)) +
  scale_y_continuous(limits = c(0,43)) +
  ggtitle("OSOBY Z NIEDOWAGĄ") +
  theme(plot.title = element_text(hjust=0.5, vjust = 1.9, size = 12))


#---------otylosc---------------
Pytanie57_12_otyl <- Pytanie57_12
Pytanie57_12_otyl$n <- (Pytanie57_12_otyl$n/sum(na.omit(
  Pytanie57_12_otyl[Pytanie57_12_otyl$BMI_ocena=='otyłość'
                    & !is.na(Pytanie57_12_otyl$HP57_12),]$n)))*100
Pytanie57_12_otyl <- Pytanie57_12_otyl[Pytanie57_12_otyl$BMI_ocena=='otyłość' & 
                                         !is.na(Pytanie57_12_otyl$HP57_12),]
Pytanie57_12_otyl <- Pytanie57_12_otyl[1:7,]

plot57_12_d <- ggplot(Pytanie57_12_otyl, aes(x = HP57_12, y = n)) +
  geom_col(fill = column_color) +
  theme_economist_white() + 
  xlab("") + 
  ylab("Procent ankietowanych") +
  theme(axis.title.y = element_text(color="black", size=14, face="bold",
                                    margin = margin(t = 0, r = 12, b = 0, l = 0))) +
  geom_text(aes(label = paste( sprintf("%0.2f",round(n,digits=3)),'%')), nudge_x = 0, vjust=-0.7,
            colour = "black", fontface = "bold")+
  scale_y_continuous(limits = c(0,43)) +
  ggtitle("OSOBY Z OTYŁOŚCIĄ") +
  theme(axis.text.x = element_text(color="black", size=10, face="bold",
                                   vjust = 0.7)) +
  theme(plot.title = element_text(hjust=0.5, vjust = 1.9, size = 12))


#---------komentarz przed wykresem---------------
# W tej sekcji zbadamy odpowiedzi ankietowanych na pytanie, czy chcieliby dobrze,
# atrakcyjnie wyglądać. Każdy z poniższych wykresów przedstawia procentowy podział
# siedmiu możliwych odpowiedzi udzielonych przez przedstawicieli poszczególnych kategorii
# masy ciała wyznaczonych przez poziom BMI.


#---------glowny wykres---------------
ggarrange(plot57_12_c, plot57_12_b, plot57_12_a, plot57_12_d, 
          labels = c("", "", "", ""),
          ncol = 2, nrow = 2) +
#  ggtitle("Chciałbym dobrze, atrakcyjnie wyglądać") +
  theme(plot.title = element_text(hjust=0.5, vjust = 1,
                                  size = 17, face = "bold"))


#---------komentarz po wykresie---------------
# Na podstawie powyższych wykresów możemy stwierdzić, że osoby z niedowagą 
# są najbardziej zdecydowane, że chciałyby atrakcyjnie wyglądać. Z kolei osoby
# z otyłością udzieliły najmniej takich odpowiedzi.  

