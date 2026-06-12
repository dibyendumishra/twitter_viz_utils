library(wordcloud)
df <- read.csv('celebs_INC.csv')
row.names(df) <- df$word
df$word <- NULL
colnames(df) <- c('Topic 1','Topic 2','Topic 3','Topic 4','Topic 5','Topic 6')
mat <-as.matrix(df)
dev.new(width=10,height=10)
comparison.cloud(mat,random.order=TRUE, scale=c(1.5,0.5),
                 colors = brewer.pal(6, "Paired"),
                 max.words=100,title.size = 1,
                 title.bg.colors = 'white')
#pdf("bjp_celebs_test.pdf", family = "CM Roman") 
