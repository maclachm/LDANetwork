#creates a network graph using D3

createGraph <- function(threshold){
  library('jsonlite')
  library(networkD3)
  
  #thres <- 0.25
  thres <- threshold
  #load JSON file output from LDA.py
  data <- fromJSON("out.json")
  range01 <- function(x){(x-min(x))/(max(x)-min(x))}
  
  #use this function to scale probabilities
  #data2$links$value <- range01(data2$links$value) 
  
  #use this to take a random sample of the links
  #d <- data2$links[sample(nrow(data2$links), 50000), ]
  d <- data$links
  d <- subset(d, d$value > thres) #set threshold for probability
  
  #network
  n <- forceNetwork(Links = d, Nodes = data$nodes,
                    Source = "source", Target = "target",
                    Value = "value", NodeID = "name",
                    Group = "topic", 
                    #linkDistance = "function(d) { return Math.sqrt(d.value); }", 
                    linkColour = "#dbdbdb",
                    opacity = 0.8)
  
  #n
  saveNetwork(n, file="network.html", selfcontained=FALSE)
}

