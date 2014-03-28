#' Download public datasets via the EcoData Retriever.
#'
#' Data is either linked to one of the following connection types:
#' MySQL, PostgreSQL, SQLite, Microsoft Access, CSV
#'
#' @param datasets the names of the datasets that you wish to download
#' @param connection what type of database connection should be used. 
#' The options include: mysql, postgres, sqlite, msaccess, or csv'
#' @param db_file the name of the datbase file the dataset should be loaded 
#' into
#' @param log_dir the location where the retriever log should be stored if 
#' the progress is not printed to the console
#' @param user the user argument for connecting data to a database server
#' @param pwd the password argument for connecting data to a database server
#' @param host the host argument for connecting data to a database server
#' @param port the port argument for connecting data to a database server
#' @export
#' @examples
#' download_public_data('MCDB', 'csv')
download_public_data = function(dataset, connection, db_file=NULL,
                                log_dir=NULL, user=NULL, pwd=NULL, host=NULL,
                                port=NULL){
  if (connection == 'mysql') {
    cmd = paste('retriever install mysql --user', user, '--password',
                pwd, '--host', host, '--port', port, dataset)
  }
  if (connection == 'postgres') {
    stop('postgres not currently supported')
  }
  if (connection == 'sqlite' | connection == 'msaccess') {
    if (is.null(db_file)) {
      if (connection == 'sqlite')
        db_file = paste(data_dir, dataset, '.db', sep='')
      else 
        db_file = paste(data_dir, dataset, '.accdb', sep='')
    }
    ## check that blank database exists when using sqlite or msaccess
    if (!file.exists(db_file))
      stop(paste('The empty database file', db_file,
                 'must exist so that the retreiver can access it'))
    else
      cmd = paste('retriever install', connection, dataset, '--file', db_file)
  }
  if (connection == 'csv') {
    cmd = paste('retriever install csv', dataset)
  }
  if (!is.null(log_dir)) {
    if (substr(log_dir, nchar(log_dir), nchar(log_dir)) != '/')
      log_dir = paste(log_dir, '/', sep='')
    log_file = paste(log_dir, dataset, '_download.log', sep='')
    cmd = paste(cmd, '>', log_file, '2>&1')
  }
  system(cmd)
}

