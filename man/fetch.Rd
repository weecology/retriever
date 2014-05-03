\name{fetch}
\alias{fetch}
\title{Fetch a dataset via the EcoData Retriever}
\usage{
fetch(dataset, quiet = TRUE)
}
\arguments{
  \item{dataset}{the name of the dataset that you wish to
  download}

  \item{quiet:}{logical, if true retriever runs in quiet
  mode}
}
\description{
Each datafile in a given dataset is downloaded to a
temporary directory and then imported as a data.frame as a
member of a named list.
}
\examples{
## fetch the Mammal Community Database (MCDB)
MCDB = fetch('MCDB')
class(MCDB)
names(MCDB)
## preview the data in the MCDB communities datafile
head(MCDB$communities)
}

