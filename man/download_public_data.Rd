\name{download_public_data}
\alias{download_public_data}
\title{Download public datasets via the EcoData Retriever.}
\usage{
download_public_data(dataset, connection, db_file = NULL, log_dir = NULL,
  user = NULL, pwd = NULL, host = NULL, port = NULL)
}
\arguments{
  \item{datasets}{the names of the datasets that you wish
  to download}

  \item{connection}{what type of database connection should
  be used. The options include: mysql, postgres, sqlite,
  msaccess, or csv'}

  \item{db_file}{the name of the datbase file the dataset
  should be loaded into}

  \item{log_dir}{the location where the retriever log
  should be stored if the progress is not printed to the
  console}

  \item{user}{the user argument for connecting data to a
  database server}

  \item{pwd}{the password argument for connecting data to a
  database server}

  \item{host}{the host argument for connecting data to a
  database server}

  \item{port}{the port argument for connecting data to a
  database server}
}
\description{
Data is either linked to one of the following connection
types: MySQL, PostgreSQL, SQLite, Microsoft Access, CSV
}
\examples{
download_public_data('MCDB', 'csv')
}

