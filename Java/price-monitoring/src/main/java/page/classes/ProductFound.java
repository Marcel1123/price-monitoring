package page.classes;

import entities.ProductEntity;
import flexjson.JSONDeserializer;
import flexjson.JSONSerializer;
import flexjson.ObjectFactory;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;

import javax.annotation.PostConstruct;
import javax.enterprise.context.RequestScoped;
import javax.faces.context.FacesContext;
import javax.inject.Named;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Named
@RequestScoped
@Getter
@Setter
public class ProductFound {
    private ProductEntity[] products;

//    @PostConstruct
//    public void init(){
//        products = new JSONDeserializer<ProductEntity[]>()
//                .use(null, ArrayList.class)
//                .use("values", ProductEntity.class)
//                .deserialize(FacesContext.getCurrentInstance().getExternalContext().getSessionMap().get("products").toString());

//        Map<String,String> parameterValue = FacesContext.getCurrentInstance().getExternalContext().getRequestParameterMap();
//        products = deserializer.deserialize(parameterValue.get("products"));
//    }
}
