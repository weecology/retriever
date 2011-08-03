# make apidocs
cd ..
sudo pydoctor --add-package=retriever --make-html
sudo mv apidocs retriever
cd retriever
