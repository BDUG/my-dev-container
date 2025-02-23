UML Example
===========

A simple sequence diagram:

.. uml::

   @startuml
   actor Developer
   participant "Sphinx CLI" as SP
   participant "Documentation" as DOC

   Developer -> SP: sphinx-quickstart
   note right: New documentation project

   Developer -> SP: sphinx-build
   note right: Build the documentation 

   SP -> DOC: Generate to pdf
   @enduml

